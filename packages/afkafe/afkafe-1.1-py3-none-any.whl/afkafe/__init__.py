import logging
import logging.config
import random
import time
from typing import Annotated

from pynput import keyboard, mouse
from terminal_shop import Terminal
from typer import Argument, Option, Typer, Exit

from .utils import default_log_config

VERSION = "1.1"

__version__ = VERSION

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

cli = Typer()


def version_callback(value: bool) -> None:
    if value:
        print(f"AFKafé v{VERSION}")
        raise Exit()


previous_event_time = time.time()


def on_event(*args):
    logger.debug(f"Received event {args}")
    global previous_event_time
    previous_event_time = time.time()


@cli.command()
def main(
    timeout: Annotated[
        int,
        Argument(
            help="Idle timeout in seconds before ordering coffee, defaults to 30 minutes"
        ),
    ] = 30 * 60,
    use_dev: Annotated[
        bool, Option("--dev", help="Use dev environment instead of production")
    ] = False,
    verbose: Annotated[
        bool,
        Option(
            "--verbose",
            help="Whether to use logging.DEBUG instead of logging.INFO",
        ),
    ] = False,
    version: Annotated[
        bool,
        Option("--version", callback=version_callback, help="Show installed version"),
    ] = False,
) -> None:
    logging.config.dictConfig(default_log_config(verbose))
    logger.debug("Big dict entered the void (of the logging config)")
    keyboard_listener = keyboard.Listener(on_press=on_event)
    mouse_listener = mouse.Listener(
        on_move=on_event, on_click=on_event, on_scroll=on_event
    )
    keyboard_listener.start()
    mouse_listener.start()
    client = Terminal(environment="dev" if use_dev else "production")
    while True:
        duration = timeout - (time.time() - previous_event_time)
        time.sleep(max(duration, 0))
        # time to order coffee!
        if previous_event_time < time.time() - timeout:
            logger.info("User needs caffeine!")
            keyboard_listener.stop()
            mouse_listener.stop()
            # random coffee that's not decaf
            product = client.product.list()
            products = [p for p in product.data if "decaf" not in p.description.lower()]
            chosen = random.choice(products)
            logger.info(f"Selected bag {chosen.name} out of desperation.")
            # use the first address/card
            address = client.address.list().data[0]
            card = client.card.list().data[0]
            order = client.order.create(
                address_id=address.id,
                card_id=card.id,
                variants={chosen.id: 1},
            )
            logger.info(f"Placed order {order.data}")
            # exit service
            raise Exit()


if __name__ == "__main__":
    main()
