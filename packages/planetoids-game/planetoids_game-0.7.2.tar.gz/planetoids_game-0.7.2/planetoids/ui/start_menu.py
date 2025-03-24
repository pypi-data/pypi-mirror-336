import random
import math

import pygame

from planetoids.core.config import config
from planetoids.entities.asteroid import BackgroundAsteroid
from planetoids.effects.crt_effect import apply_crt_effect  # Import CRT effect function
from planetoids.core.logger import logger
from planetoids.ui.options_menu import OptionsMenu
from planetoids.core.version_checker import check_for_update

class StartMenu:
    def __init__(self, screen, clock, settings):
        """Initialize the start menu with a moving asteroid background and refined retro font."""
        self.screen = screen
        self.clock = clock
        self.running = True
        self.selected_index = 0
        self.menu_items = ["Start Game", "Options", "Quit"]
        self.settings = settings

        # Load a refined vintage arcade font (Sleek but retro)
        self.menu_font = pygame.font.Font(self.settings.FONT_PATH, 64)
        self.small_font = pygame.font.Font(self.settings.FONT_PATH, 36)

        # Initialize Options Menu
        self.options_menu = OptionsMenu(
            self.screen, self.settings, self.font, self.menu_font, self.small_font
        )

        # Generate background asteroids
        self.background_asteroids = [
            BackgroundAsteroid(
                None,
                random.randint(0, config.WIDTH),
                random.randint(0, config.HEIGHT),
                size=random.randint(30, 60),
                stage=3)
            for _ in range(5)
        ]
        logger.info("StartMenu instantiated")

        self.latest_version = None
        check_for_update(config.VERSION, self._on_new_version_found)

    @property
    def font(self):
        return pygame.font.Font(
            self.settings.FONT_PATH,
            {"minimum": 36, "medium": 48, "maximum": 64}.get(self.settings.get("pixelation"), 36)
        )

    def _on_new_version_found(self, latest_version):
        self.latest_version = latest_version

    def show(self):
        """Displays the start menu with moving asteroid background using delta time."""
        logger.info("Show start menu")

        while self.running:
            dt = self.clock.tick(60) / 1000.0

            self.screen.fill(config.BLACK)
            for asteroid in self.background_asteroids:
                asteroid.update(dt)

                asteroid.draw(self.screen)

            self._draw_main_menu()

            if self.settings.get("crt_enabled"):
                apply_crt_effect(
                    self.screen,
                    intensity=self.settings.get("glitch_intensity"),
                    pixelation=self.settings.get("pixelation")
                )

            pygame.display.flip()
            self._handle_events()

        self._fade_out()

    def _draw_main_menu(self):
        """Draws the main start menu with a refined arcade look."""
        title_font = pygame.font.Font(
            self.settings.FONT_PATH,
            200
        )
        title_surface = title_font.render("PLANETOIDS", True, config.YELLOW)
        title_rect = title_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 3))
        self.screen.blit(title_surface, title_rect)

        if self.latest_version:
            update_msg = f"New version available: v{self.latest_version}!"
            update_text = self.font.render(update_msg, True, config.YELLOW)
            update_rect = title_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 3 + 175))
            self.screen.blit(update_text, update_rect)

        for i, item in enumerate(self.menu_items):
            color = config.WHITE if i != self.selected_index else config.ORANGE  # Highlight selected option
            self._draw_text(item, config.WIDTH // 2 - 120, config.HEIGHT // 2 + i * 50, color, self.menu_font)

        x_offset = {"minimum": 0, "medium": 30, "maximum": 60}.get(self.settings.get("pixelation"), 40)
        y_offset = {"minimum": 45, "medium": 60, "maximum": 75}.get(self.settings.get("pixelation"), 40)
        text_surface = self.font.render("Press ENTER to select", True, config.DIM_GRAY)
        text_width = text_surface.get_width()
        self._draw_text("Press ENTER to select", (config.WIDTH - text_width) // 2 + x_offset, config.HEIGHT - y_offset, config.DIM_GRAY, self.font)
        self._draw_studio_branding()
        self._draw_version()

    def _draw_version(self):
        """Displays the game version in the bottom right corner."""
        version_text = self.font.render(config.VERSION, True, config.DIM_GRAY)
        version_rect = version_text.get_rect(bottomright=(config.WIDTH - 10, config.HEIGHT - 10))
        self.screen.blit(version_text, version_rect)

    def _draw_studio_branding(self):
        """Displays 'Greening Studio' in the bottom left corner."""
        studio_text = self.font.render("GREENING STUDIO", True, config.GREEN)
        studio_rect = studio_text.get_rect(bottomleft=(10, config.HEIGHT - 10))
        self.screen.blit(studio_text, studio_rect)

    def _draw_text(self, text, x, y, color=config.WHITE, font=None):
        """Helper function to render sharp, readable text."""
        if font is None:
            font = self.font  # Default to main font
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))

    def _handle_events(self):
        """Handles user input for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    self._handle_main_selection()

    def _handle_main_selection(self):
        """Handles selection in the main menu."""
        if self.selected_index == 0:  # Start Game
            self.running = False  # Exit menu loop
        elif self.selected_index == 1:  # Open Options
            self.options_menu.show()
        elif self.selected_index == 2:  # Quit
            pygame.quit()
            exit()

    def _fade_out(self):
        """Applies a fade-out transition before starting the game using delta time."""
        fade_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        fade_surface.fill(config.BLACK)

        alpha = 0  # Start from fully transparent
        fade_speed = 150  # Adjust this for faster/slower fade (higher = faster)

        while alpha < 255:
            dt = self.clock.tick(60) / 1000.0

            alpha += fade_speed * dt
            fade_surface.set_alpha(min(255, int(alpha)))
            self.screen.fill(config.BLACK)

            for asteroid in self.background_asteroids:
                asteroid.update(dt)
                asteroid.draw(self.screen)

            if self.settings.get("crt_enabled"):
                apply_crt_effect(self.screen, self.settings)

            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
