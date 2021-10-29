from celery import shared_task


@shared_task
def test(a, b):
    return a + b
