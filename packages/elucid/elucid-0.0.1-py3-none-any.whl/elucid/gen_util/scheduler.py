from typing import Any, Iterable, List
from pyhipp.core import abc
from dataclasses import dataclass
import numpy as np


class Job(abc.HasDictRepr):
    pass
        
class IndexedJob(Job):
    
    repr_attr_keys = ('id',)
    
    def __init__(self, id: int, **kw) -> None:
        super().__init__(**kw)
        self.id = id
    

class JobList(abc.HasDictRepr):
    
    JobType: type = Job
    
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
    
    def __iter__(self) -> Iterable[JobType]:
        raise NotImplementedError()
        
class IndexedJobList(JobList):
    
    JobType: type = IndexedJob
    repr_attr_keys = ('id_list', 'size')
    
    def __init__(self, id_list: List[int],  **kw) -> None:
        super().__init__(**kw)
        self.id_list = id_list
    
    @property
    def size(self) -> int:
        return len(self.id_list)
    
    def __iter__(self) -> Iterable[JobType]:
        JobType = self.JobType
        for id in self.id_list:
            yield JobType(id)
    
    def __len__(self) -> int:
        return self.size
    
    def __getitem__(self, i: int) -> JobType:
        return self.JobType(self.id_list[i])

class Scheduler(abc.HasDictRepr):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        
class StaticScheduler(Scheduler):
    '''
    n_jobs and the the jobs of each worker are determined at the construction 
    time.
    '''
    
    repr_attr_keys = ('n_jobs', 'n_workers', 'pl')
    
    @dataclass
    class Policy:
        batch_size: int     = 0
    
    def __init__(self, n_jobs: int, n_workers: int, pl: Policy = None,
                 **kw) -> None:
        
        super().__init__(**kw)
        
        assert n_workers > 0
        if pl is None:
            pl = StaticScheduler.Policy()
            
        self.n_jobs = n_jobs
        self.n_workers = n_workers
        self.pl = pl
        
    @property
    def used_batch_size(self):
        bsz = self.pl.batch_size
        if bsz > 0:
            return bsz
        n_jobs, n_workers = self.n_jobs, self.n_workers
        return (n_jobs + n_workers - 1) // self.n_workers
            
    def jobs(self, worker_id: int) -> IndexedJobList:
        '''
        @worker_id: an index in [0, n_workers). Negative values are allowed.
        '''
        bsz, n_jobs, n_workers = (self.used_batch_size, 
                                  self.n_jobs, self.n_workers)
        group_bsz = n_workers * bsz
        if worker_id < 0:
            worker_id = n_workers + worker_id
        assert worker_id < n_workers and worker_id >= 0
        
        job_id_list = []
        group_b = 0
        while group_b < n_jobs:
            group_e = group_b + group_bsz
            if group_e <= n_jobs:    
                b = group_b + worker_id * bsz   
                e = b + bsz
            else:
                n_jobs_left = n_jobs - group_b
                bsz = n_jobs_left // n_workers
                n_jobs_left -= bsz * n_workers
                if worker_id < n_jobs_left:
                    b = group_b + worker_id * (bsz + 1)
                    e = b + bsz + 1
                else:
                    b = group_b + n_jobs_left + worker_id * bsz
                    e = b + bsz
            job_id_list.append(np.arange(b, e))
            group_b = group_e
            
        return IndexedJobList(np.concatenate(job_id_list))
        
        
        