from django_q.models import Schedule
from projects.models import Simulation
from projects.requests import check_mvs_simulation
from projects.constants import PENDING
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)

r"""Functions meant to be powered by Django-Q.

Those functions require Django-Q cluster to run along with Django Server.
To achieve this `python manage.py qcluster` command needs to be executed.

"""

def check_simulation_objects(**kwargs):
    pending_simulations = Simulation.objects.filter(status=PENDING)
    if pending_simulations.count() == 0:
        logger.debug(f"No pending simulation found. Deleting Scheduler.")
        Schedule.objects.all().delete()
    # check_mvs_simulation mostly waits for MVS API to respond, so no ProcessPool is required.
    with ThreadPoolExecutor() as pool:
        pool.map(check_mvs_simulation, pending_simulations)
    logger.debug(f"Finished round for checking Simulation objects status.")


def create_or_delete_simulation_scheduler(**kwargs):
    r"""Initialize a Django-Q Scheduler for all Simulation objects.

    If there are Simulation objects in the database, being in "PENDING" state
    a Scheduler is created to check periodically each Simulation (utilizes MVS API).
    If there is no Simulation is "PENDING" state the Scheduler object is deleted.

    Parameters
    ----------
    **kwargs : dict
        Possible future keyword arguments.
    
    Returns
    -------
    bool :
        True if Scheduler object is created or False otherwise.

    """
    if Schedule.objects.count() == 0:
        logger.info(f"No Scheduler found. Creating a new Scheduler to check Simulation objects.")
        schedule = Schedule.objects.create(
            name="djangoQ_Scheduler",
            func="projects.services.check_simulation_objects",
            # args='5',
            schedule_type=Schedule.MINUTES,
            minutes=1
            # kwargs={'test_arg': 1, 'test_arg2': "test"}
        )
        if schedule.id:
            logger.info(f"New Scheduler Created to track simulation objects status.")
            return True
        else:
            logger.debug(f"Scheduler already exists. Skipping.")
            return False
