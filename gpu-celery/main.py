from broker import celery
from time import sleep
from celery import states
import traceback

@celery.task(name='gpu.task', bind=True)
def gpu(self, number):
    try:
        if number == 0:
            number = 1 / number ## this is only to check the error message

        for i in range(number):
            sleep(1)
            self.update_state(state='PROGRESS', meta={'done': i, 'total': number})
        return {"result": "{} times run gpu task".format(str(number))}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex