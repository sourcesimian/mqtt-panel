from mqtt_panel.mqtt import TopicMatcher


class TestTopicMatcher:
    def test_basic(self):
        assert TopicMatcher('topic/one').match('topic/one') == True
        assert TopicMatcher('topic/two').match('topic/one') == False

    def test_plus(self):
        assert TopicMatcher('topic/+/plus').match('topic/one/plus') == True
        assert TopicMatcher('topic/+/plus').match('topic/one/extra/plus') == False
        assert TopicMatcher('++/plus').match('topic/one/plus') == False
        assert TopicMatcher('+one/plus').match('topic/one/plus') == False
        assert TopicMatcher('+ne/plus').match('one/plus') == False

    def test_hash(self):
        assert TopicMatcher('#').match('topic/one/plus') == True
        assert TopicMatcher('topic/#').match('topic/one/plus') == True
        assert TopicMatcher('topic/two/#').match('topic/one/plus') == False
        assert TopicMatcher('#/plus').match('one/plus') == False

    def test_plus_and_hash(self):
        assert TopicMatcher('+/+/plus/#').match('topic/one/plus/many/more') == True
        assert TopicMatcher('+/+/minus/#').match('topic/one/plus/many/more') == False
