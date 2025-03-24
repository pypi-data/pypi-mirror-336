import redis
import random
import string
import threading
import json
from typing import Callable
from simple_parsing import parse
from dataclasses import dataclass
from contextlib import contextmanager
from pathlib import Path

BYTES_IN_MB = 1024 * 1024
JSON_PATH = str(Path(__file__).parent / "distributions.json")

@contextmanager
def exception_wrapper():
    """
    Suppresses ResponseError exceptions that are expected to occur during the execution of 
    randomally generated Redis commands. All other exceptions are raised.
    """
    try:
        yield
    except redis.exceptions.ResponseError as e:
        if ("WRONGTYPE" not in str(e)) and (not ("INCRBY" in str(e) and "value is not an integer or out of range" in str(e))):
            raise e

class RedisObj():
    """
    A wrapper class for the redis.Redis client that intercepts method calls
    and wraps them in an exception handling context manager.
    """

    def __init__(self, *args, **kwargs):
        self._client = redis.Redis(*args, **kwargs)

    def __getattr__(self, name):
        """
        Retrieves the attribute from the underlying Redis client. If the attribute
        is callable, it wraps the method call in the exception_wrapper context manager.
        """
        original_attr = getattr(self._client, name)

        if callable(original_attr):
            def wrapper(*args, **kwargs):
                with exception_wrapper():
                    return original_attr(*args, **kwargs)
            return wrapper
        else:
            return original_attr

@dataclass
class BaseGen():
    verbose: bool = False  # Print debug information (sent commands)
    hosts: tuple = ("localhost:6379",)  # Redis hosts to connect to
    flush: bool = False  # Flush all hosts on connection
    max_cmd_cnt: int = 10000  # Maximum number of commands to execute, may be interrupted by exceeding memory cap. Set to 0 for infinite
    mem_cap: float = 70  # Memory cap percentage
    pipe_every_x: int = 1000  # Execute pipeline every X commands
    def_key_size: int = 10  # Default key size
    def_key_pref: str = '' # Default key prefix
    distributions: str = None # distributions.json file path or a serialized dict (e.g. {"expire": 50, "incrby": 70, ...})
    logfile: str = None  # Optional log file path to write debug information to
    maxmemory_mb: int = None  # Override INFO's maxmemory (useful when unavailable, for e.g. in cluster mode)
    print_prefix: str = "COMMAND GENERATOR: "
    
    ttl_low: int = 15
    ttl_high: int = 300

    ########################################
    ######## Internal use methods ##########
    ########################################

    def _rand_str(self, str_size: int) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k = str_size))
    
    def _rand_key(self) -> str:
        return self.def_key_pref + self._rand_str(self.def_key_size)
    
    def _scan_rand_key(self, redis_obj: redis.Redis, type: str) -> str | None:
        if not hasattr(self, 'scan_cursors'):
            self.scan_cursors = {}
        
        conn = self._get_conn_info(redis_obj)
        if conn not in self.scan_cursors:
            self.scan_cursors[conn] = {}
        
        if type not in self.scan_cursors[conn]:
            self.scan_cursors[conn][type] = 0
        
        cursor, keys = redis_obj.scan(self.scan_cursors[conn][type], _type=type)
        self.scan_cursors[conn][type] = cursor
        return random.choice(keys) if keys else None
    
    def _get_rand_cmd(self) -> Callable[[redis.client.Pipeline, str], None]:
        name = random.choices(list(self.distributions.keys()), weights=list(self.distributions.values()))[0]
        return getattr(self, name)
    
    def _check_mem_cap(self, redis_obj: redis.Redis):
        info = redis_obj.info()
        
        if self.maxmemory_mb:
            max_mem = self.maxmemory_mb * BYTES_IN_MB
        else:
            max_mem = info['maxmemory'] if ('maxmemory' in info) else None
        
        curr_mem = info['used_memory']
        
        if max_mem and curr_mem >= (self.mem_cap / 100) * max_mem:
            self._print(f"Memory cap for {self._get_conn_info(redis_obj)} reached, with {curr_mem} bytes used out of {max_mem * (self.mem_cap / 100)} available")
            return True
        else:
            return False
    
    def _get_conn_info(self, redis_obj: redis.Redis) -> str:
        return f"{redis_obj.connection_pool.connection_kwargs['host']}:{redis_obj.connection_pool.connection_kwargs['port']}"
    
    def _pipe_to_redis(self, pipe: redis.client.Pipeline) -> RedisObj:
        return RedisObj(connection_pool=pipe.connection_pool)
    
    def _print(self, msg: str) -> None:
        if self.file:
            self.file.write(f"{msg}\n")
        
        if self.verbose:
            print(self.print_prefix + msg)
    
    def _extract_distributions(self) -> None:
        if self.distributions is None:
            self.distributions = JSON_PATH
        
        if self.distributions.endswith('.json'):
            with open(self.distributions, 'r') as f:
                self.distributions = json.load(f)
        else:
            self.distributions = json.loads(self.distributions)
        
        method_names = [name for name in dir(self) if callable(getattr(self, name)) and not name.startswith('_')]
        for cmd in self.distributions:
            if cmd not in method_names:
                raise ValueError(f"Command '{cmd}' not found in generator")
    
    def _run(self, stop_event: threading.Event = None) -> None:
        self.file = open(self.logfile, 'w') if self.logfile else None
        rl = []  # Redis connections list
        redis_pipes = []
        
        try:
            self._extract_distributions()
            
            for host in self.hosts:
                (hostname, port) = host.split(':')
                r = redis.Redis(host=hostname, port=port)
                r.ping()
                
                if self.flush:
                    r.flushall()
                self._print("INFO: " + str(r.info()))
                
                rl.append(r)
                redis_pipes.append(r.pipeline(transaction=False))
            
            i = 1
            while self.max_cmd_cnt == 0 or i <= self.max_cmd_cnt:
                if stop_event and stop_event.is_set():
                    break
                for r in rl:
                    if self._check_mem_cap(r):
                        return
                
                key = self._rand_key()
                cmd = self._get_rand_cmd()
                
                for pipe in redis_pipes:
                    cmd(pipe, key)

                if i % self.pipe_every_x == 0:
                    for (pipe, r) in zip(redis_pipes, rl):
                        self._print(f"Executing pipeline for {self._get_conn_info(r)}")
                        for command in pipe.command_stack:
                            self._print(f"Command: {command[0]}")
                        
                        with exception_wrapper():
                            pipe.execute()
                
                i += 1
            
            # Execute remaining commands
            for pipe in redis_pipes:
                with exception_wrapper():
                    pipe.execute()
        
        except Exception as e:
            self._print(f"Exception: {e}")
            raise e
        
        finally:
            for r in rl:
                self._print("Connection: " + self._get_conn_info(r))
                self._print("Memory usage: " + str(r.info()['used_memory']))
                self._print("DB size: " + str(r.dbsize()))
                r.close()
            self.file.close() if self.file else None
    
    ########################################
    ######## Redis command methods #########
    ########################################
    
    def expire(self, pipe: redis.client.Pipeline, key: str = None, replace_nonexist: bool = True) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        
        if key is None or (replace_nonexist and not redis_obj.exists(key)):
            key = redis_obj.randomkey()
        if not key: return
        
        pipe.expire(key, random.randrange(self.ttl_low, self.ttl_high))
    
    def persist(self, pipe: redis.client.Pipeline, key: str = None, replace_nonexist: bool = True) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        
        if key is None or (replace_nonexist and not redis_obj.exists(key)):
            key = redis_obj.randomkey()
        if not key: return
        
        pipe.persist(key)

if __name__ == "__main__":
    base_gen = parse(BaseGen)
    base_gen.distributions = '{"expire": 100, "persist": 100}'
    base_gen._run()