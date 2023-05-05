from django.test import TestCase

from notebook.models import Note
from django.contrib.auth.models import User


class NoteTestCase(TestCase):

    def setUp(self):
        
        # Creates, saves, returns user
        testAuthor = User.objects.create_user("testusername", "test@test.com", "testpassword")

        # Create a note entry 
        Note.objects.create(title="test", content="test content", author=testAuthor)

    def test_note_in_database(self):

        # Checking if note is in database
        self.assertTrue(Note.objects.filter(title="test", content="test content").exists())

    def test_note_create(self):

        # Getting both objects
        testNote = Note.objects.get(title="test", content="test content")
        testAuthor = User.objects.get(username="testusername")

        # Testing data fields
        self.assertEqual(testNote.title, "test")
        self.assertEqual(testNote.content, "test content")
        self.assertEqual(testNote.author, testAuthor)
        self.assertEqual(testNote.id, 1)
        self.assertEqual(testNote.slug, "")

    def test_note_str(self):

        # Get note
        testNote = Note.objects.get(title="test")

        expected = "test by testusername"

        self.assertEqual(testNote.__str__(), expected)

    def test_note_delete(self):

        # Delete note
        Note.objects.get(title="test", content="test content").delete()

        self.assertFalse(Note.objects.filter(title="test", content="test content").exists())
