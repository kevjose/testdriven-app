from tasks import celery
import time

@celery.task(name='tasks.super_add_task', bind=True)
def add(self, x: int, y: int) -> int:
    self.update_state(state='PROGRESS',
                      meta={'status': "Started the timer"})
    time.sleep(300)
    self.update_state(state='PROGRESS',
                      meta={'status': "About to return"})
    time.sleep(120)
    return x + y