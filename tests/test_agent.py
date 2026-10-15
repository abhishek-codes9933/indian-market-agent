import unittest
from unittest.mock import patch
from datetime import datetime
import market_agent as a

class AgentTests(unittest.TestCase):
    def test_unicode_chunks(self):
        text = 'Market 📈' * 1500
        parts = list(a.chunks(text))
        self.assertEqual(''.join(parts), text)
        self.assertTrue(all(len(p.encode('utf-16-le')) // 2 <= 3500 for p in parts))

    def test_stale_news_excluded(self):
        raw = b'<rss><channel><item><title>Old</title><link>https://example.com</link><pubDate>Mon, 12 Oct 2026 02:00:00 GMT</pubDate></item></channel></rss>'
        self.assertEqual(a.parse_feed(raw, 'Test', datetime(2026, 10, 15, 9, tzinfo=a.IST)), [])

    def test_failed_ai_falls_back(self):
        items = [{'title': 'Source headline', 'url': 'https://example.com', 'source': 'Test', 'published': '2026-10-15T08:00:00+05:30'}]
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'fake'}), patch.object(a, 'collect_news', return_value=(items, [])), patch.object(a, 'summarize', side_effect=a.ServiceError('HTTP 429')):
            report = a.build_report(datetime(2026, 10, 15, 9, tzinfo=a.IST))
        self.assertIn('AI unavailable', report)
        self.assertIn('Source headline', report)

    def test_rejected_delivery_fails(self):
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'fake', 'TELEGRAM_CHAT_ID': '123'}), patch.object(a, 'request', return_value=b'{"ok":false}'):
            with self.assertRaises(a.ServiceError):
                a.send_telegram('test')

    def test_uncited_ai_rejected(self):
        response = b'{"candidates":[{"finishReason":"STOP","content":{"parts":[{"text":"Uncited claims"}]}}]}'
        with patch.object(a, 'request', return_value=response):
            with self.assertRaises(a.ServiceError):
                a.summarize([{'title': 'Headline'}], 'fake')
