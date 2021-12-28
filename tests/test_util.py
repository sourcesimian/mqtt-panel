
from mqtt_panel.util import check_mqtt_topic_matches_pattern

class TestCheckMqttTopicPattern:
    def test_clean_pattern_success(self):
        assert check_mqtt_topic_matches_pattern('topic/one', 'topic/one') == True
    
    def test_clean_pattern_fail(self):
        assert check_mqtt_topic_matches_pattern('topic/one', 'topic/two') == False
    
    def test_single_slot_pattern_success(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus', 'topic/+/plus') == True
    
    def test_single_slot_pattern_fail(self):
        assert check_mqtt_topic_matches_pattern('topic/one/extra/plus', 'topic/+/plus') == False
    
    def test_hash_pattern_success(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus', '#') == True
    
    def test_trailing_hash_pattern_success(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus', 'topic/#') == True
    
    def test_trailing_hash_pattern_fail(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus', 'topic/two/#') == False
    
    def test_multiple_pattern_success(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus/many/more', '+/+/plus/#') == True
    
    def test_multiple_pattern_fail(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus/many/more', '+/+/minus/#') == False
    
    def test_invalid_pattern_bad_plus_1(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus', '++/plus') == False
    
    def test_invalid_pattern_bad_plus_2(self):
        assert check_mqtt_topic_matches_pattern('topic/one/plus', '+one/plus') == False
    
    def test_invalid_pattern_bad_plus_3(self):
        assert check_mqtt_topic_matches_pattern('one/plus', '+ne/plus') == False
    
    def test_invalid_pattern_bad_hash(self):
        assert check_mqtt_topic_matches_pattern('one/plus', '#/plus') == False
