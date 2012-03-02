# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Resource'
        db.create_table('api_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource_identifier', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('api', ['Resource'])

        # Adding M2M table for field resources on 'Client'
        db.create_table('api_client_resources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['api.client'], null=False)),
            ('resource', models.ForeignKey(orm['api.resource'], null=False))
        ))
        db.create_unique('api_client_resources', ['client_id', 'resource_id'])


    def backwards(self, orm):
        
        # Deleting model 'Resource'
        db.delete_table('api_resource')

        # Removing M2M table for field resources on 'Client'
        db.delete_table('api_client_resources')


    models = {
        'api.client': {
            'Meta': {'object_name': 'Client'},
            'api_key': ('django.db.models.fields.SlugField', [], {'default': "'345da888318d96d7a7344298fff86f30'", 'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'clients'", 'symmetrical': 'False', 'to': "orm['api.Resource']"}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'9a73143126cd3ecc6750e2602ea7dceb79e97927baf2c5251d'", 'max_length': '100'})
        },
        'api.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource_identifier': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['api']
