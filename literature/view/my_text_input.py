import pygame
import pygame.locals as pl

from literature.view.global_constants import *

class Text_box:
    def __init__(self,
            box_size, # a tuple, (width, height)
            box_color,
            initial_string="",
            font_family="",
            font_size=35,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 0),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=12):

        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.input_string = initial_string  # Inputted text
        
        self.box_size = box_size

        #self.font_object = pygame.font.Font(font_family, font_size)
        self.font_object = pygame.font.Font(None, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface(box_size)
        self.surface.fill(box_color)
        self.rect = self.surface.get_rect()

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                #self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
#                if event.key not in self.keyrepeat_counters:
#                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

#            elif event.type == pl.KEYUP:
#                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
#                if event.key in self.keyrepeat_counters:
#                    del self.keyrepeat_counters[event.key]

        # Update key counters:
#        for key in self.keyrepeat_counters:
#            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock
#
#            # Generate new key events if enough time has passed:
#            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
#                self.keyrepeat_counters[key][0] = (
#                    self.keyrepeat_intial_interval_ms
#                    - self.keyrepeat_interval_ms
#                )
#
#                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
#                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        self.surface = self.font_object.render(self.input_string, True, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_text(self):
        return self.input_string

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0



#def name():
#    pygame.init()
#    screen = pygame.display.set_mode((480, 360))
#    name = ""
#    font = pygame.font.Font(None, 50)
#    while True:
#        for evt in pygame.event.get():
#            if evt.type == KEYDOWN:
#                if evt.unicode.isalpha():
#                    name += evt.unicode
#                elif evt.key == K_BACKSPACE:
#                    name = name[:-1]
#                elif evt.key == K_RETURN:
#                    name = ""
#            elif evt.type == QUIT:
#                return
#        screen.fill((0, 0, 0))
#        block = font.render(name, True, (255, 255, 255))
#        rect = block.get_rect()
#        rect.center = screen.get_rect().center
#        screen.blit(block, rect)
#        pygame.display.flip()
#
#if __name__ == "__main__":
#    name()
#    pygame.quit()