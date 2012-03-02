# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Membership'
        db.create_table('memberships_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['projects.Project'])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['profiles.Profile'])),
        ))
        db.send_create_signal('memberships', ['Membership'])


    def backwards(self, orm):
        
        # Deleting model 'Membership'
        db.delete_table('memberships_membership')


    models = {
        'memberships.membership': {
            'Meta': {'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': "orm['profiles.Profile']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': "orm['projects.Project']"})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'profiles'", 'symmetrical': 'False', 'to': "orm['projects.Project']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['memberships']
