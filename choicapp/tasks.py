from celery import shared_task
from celery.utils.log import get_task_logger
from tedok import settings

logger = get_task_logger(__name__)


@shared_task
def deliver_dokp():
    '''
    Give to each user n dok per day
    '''
    logger.info('Starting the dok delivery!')
    n = settings.DOK_DELIVERY
    try:
        from choicapp.models import Voter
        for v in Voter.objects.all():
            v.dokp += n
            v.save()
    except Exception as e:
        logger.info('Problem when delivering dokp: %s' % e)
