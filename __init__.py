import random
from os.path import join, abspath, dirname

from ovos_utils.parse import match_one
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill


class BedtimeStories(OVOSSkill):

    def initialize(self):

        # Register list of story titles that are held in a padatious entity
        self.register_entity_file("title.entity")

        # Build story list
        self.play_list = {
            'twas the night before christmas':
                join(abspath(dirname(__file__)), 'stories',
                     'twas_the_night_before_christmas.mp3'),
            'little red riding hood':
                join(abspath(dirname(__file__)), 'stories',
                     'little_red_riding_hood.mp3'),
            'the three bears':
                join(abspath(dirname(__file__)), 'stories', 'the_three_bears.mp3'),
            'hansel and gretel':
                join(abspath(dirname(__file__)), 'stories',
                     'hansel_and_gretel.mp3'),
            'the velveteen rabbit':
                join(abspath(dirname(__file__)), 'stories',
                     'the_velveteen_rabbit.mp3'),
            'rumplestiltskin':
                join(abspath(dirname(__file__)), 'stories', 'rumplestiltskin.mp3'),
            'the emporers new clothes':
                join(abspath(dirname(__file__)), 'stories',
                     'the_emporers_new_clothes.mp3'),
            'the princess and the pea':
                join(abspath(dirname(__file__)), 'stories',
                     'the_princess_on_the_pea.mp3'),
            'the elves and the shoemaker':
                join(abspath(dirname(__file__)), 'stories',
                     'the_elves_and_the_shoemaker.mp3'),
            'the three billy goats gruff':
                join(abspath(dirname(__file__)), 'stories',
                     'the_three_billy_goats_gruff.mp3'),
            'peter rabbit':
                join(abspath(dirname(__file__)), 'stories', 'peter_rabbit.mp3'),
        }

    # Play random story from list
    @intent_handler('stories.bedtime.intent')
    def handle_stories_bedtime(self, message):
        #        wait_while_speaking() # TODO - DEPRECATED
        self.speak_dialog('stories.bedtime')
        story_file = list(self.play_list.values())
        story_file = random.choice(story_file)
        self.play_audio(story_file)

    # Pick story by title
    @intent_handler('pick.story.intent')
    def handle_pick_story(self, message):
        self.speak_dialog('pick.story', wait=True)
        title = message.data.get('title')
        score = match_one(title, self.play_list)
        if score[1] > 0.5:
            self.play_audio(score[0])
        else:
            self.speak('Sorry I could not find that story in my library')
            return None

    # List stories in library
    @intent_handler('list.stories.intent')
    def handle_list_stories(self, message):
        story_list = list(self.play_list.keys())
        self.speak_dialog('list.stories', data=dict(stories=story_list))
