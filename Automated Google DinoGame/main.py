from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


JUMP_DISTANCE = 100

def main():

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    driver.get("https://chromedino.com/")

    time.sleep(2)

    # Accept consent
    consent = driver.find_element(
        By.XPATH,
        "//button[@aria-label='Consent']"
    )
    consent.click()

    # Start game
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.SPACE)

    print("Game started.")
    print("Dino bot running...")
    print("Jump distance:", JUMP_DISTANCE)

    time.sleep(1)

    # Give every cactus a permanent ID
    driver.execute_script("""
        window.__dinoObstacleIds = new WeakMap();
        window.__dinoNextObstacleId = 1;
    """)

    jumped_obstacles = set()

    # Main loop
    while True:
        game_state = driver.execute_script("""
            const game = Runner.instance_;
            const trex = game.tRex;

            if (!game || !trex) {
                return null;
            }

            const obstacles = game.horizon.obstacles.map(obstacle => {

                if (!window.__dinoObstacleIds.has(obstacle)) {
                    window.__dinoObstacleIds.set(
                        obstacle,
                        window.__dinoNextObstacleId++
                    );
                }

                return {
                    id: window.__dinoObstacleIds.get(obstacle),
                    x: obstacle.xPos
                };
            });

            return {
                crashed: game.crashed,
                dinoX: trex.xPos,
                jumping: trex.jumping,
                obstacles: obstacles
            };
        """)

        if game_state is None:
            continue

        # Game over
        if game_state["crashed"]:
            print("Game over!")
            break

        dino_x = game_state["dinoX"]
        jumping = game_state["jumping"]

        # Find cacti ahead of the Dino
        upcoming = [
            obstacle
            for obstacle in game_state["obstacles"]
            if obstacle["x"] > dino_x
        ]

        if upcoming:
            # Find nearest cactus
            obstacle = min(
                upcoming,
                key=lambda obstacle: obstacle["x"]
            )

            obstacle_id = obstacle["id"]
            distance = obstacle["x"] - dino_x

            # Jump
            if (
                distance <= JUMP_DISTANCE
                and not jumping
                and obstacle_id not in jumped_obstacles
            ):

                body.send_keys(Keys.SPACE)

                jumped_obstacles.add(obstacle_id)

        time.sleep(0.01)

    input("\nPress Enter to close Chrome...")
    driver.quit()


if __name__ == "__main__":
    main()