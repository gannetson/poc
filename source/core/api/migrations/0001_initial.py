# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Client'
        db.create_table('api_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('api_key', self.gf('django.db.models.fields.SlugField')(default='c7ade0b96a07db663d15741f708439c1', unique=True, max_length=32, db_index=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='9b52b3a25b9ca2ce53eecb36b0a94e9ae2ff7c3b428c2b1352', max_length=100)),
        ))
        db.send_create_signal('api', ['Client'])


    def backwards(self, orm):
        
        # Deleting model 'Client'
        db.delete_table('api_client')


    models = {
        'api.client': {
            'Meta': {'object_name': 'Client'},
            'api_key': ('django.db.models.fields.SlugField', [], {'default': "'f8dd19b48aa89c2a06646919a6726f05'", 'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'0ca8794a1b399030e136a6a8df183d4f61a8aeb3fcef1b8b7b'", 'max_length': '100'})
        }
    }

    complete_apps = ['api']
