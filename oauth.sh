#! /bin/bash



cd ~
git clone https://github.com/ObjectIsAdvantag/webex-integration-admin
cd ~/webex-integration-admin
npm install

#After creating your webex integration modify params here to generate new oath requests.

#FULL TOKEN
#DEBUG=oauth* PORT=9090 REDIRECT_URI="http://localhost:9090/oauth" CLIENT_ID="C1785e7c046756972f8e8b3dfc2540b7013d6c6a779628c4889ee1bba20b759ee" CLIENT_SECRET="9ccb26cb5b3c8faccf77b12c3d166dca58c69dd8cc4303f633c89f99d9f54ea4" SCOPES="meeting:schedules_read meeting:schedules_write meeting:recordings_read meeting:recordings_write meeting:preferences_read meeting:preferences_write meeting:controls_read meeting:controls_write meeting:participants_read meeting:participants_write meeting:admin_participants_read meeting:admin_schedule_read meeting:admin_schedule_write meeting:admin_recordings_read meeting:admin_recordings_write meeting:admin_preferences_write meeting:admin_preferences_read spark:calls_read spark:devices_read spark:devices_write spark:memberships_read spark:memberships_write spark:messages_read spark:messages_write spark:organizations_read spark:people_read spark:people_write spark:places_read spark:places_write spark:rooms_read spark:rooms_write spark:team_memberships_read spark:team_memberships_write spark:teams_read spark:teams_write spark:xapi_statuses spark:xapi_commands spark-admin:devices_read spark-admin:devices_write spark-admin:licenses_read spark-admin:organizations_read spark-admin:organizations_write spark-admin:people_read spark-admin:people_write spark-admin:places_read spark-admin:places_write spark-admin:resource_group_memberships_read spark-admin:resource_group_memberships_write spark-admin:resource_groups_read spark-admin:roles_read spark-admin:call_qualities_read spark-admin:workspaces_read spark-admin:workspaces_write spark-compliance:events_read spark-compliance:memberships_read spark-compliance:memberships_write spark-compliance:messages_read spark-compliance:messages_write spark-compliance:rooms_read spark-compliance:rooms_write spark-compliance:team_memberships_read spark-compliance:team_memberships_write spark-compliance:teams_read spark-admin:broadworks_enterprises_read identity:placeonetimepassword_create spark:calls_write spark-admin:hybrid_clusters_read spark-admin:hybrid_connectors_read spark-admin:broadworks_subscribers_read spark-admin:broadworks_subscribers_write analytics:read_all audit:events_read"  node static.js

#reporting account meeting statistics
DEBUG=oauth* PORT=9090 REDIRECT_URI="http://localhost:9090/oauth" CLIENT_ID="C1785e7c046756972f8e8b3dfc2540b7013d6c6a779628c4889ee1bba20b759ee" CLIENT_SECRET="9ccb26cb5b3c8faccf77b12c3d166dca58c69dd8cc4303f633c89f99d9f54ea4" SCOPES="meeting:admin_participants_read meeting:admin_schedule_read spark-admin:people_read" node static.js

# automation create + own meetings report  spark-compliance:events_read spark-compliance:rooms_read
#DEBUG=oauth* PORT=9090 REDIRECT_URI="http://localhost:9090/oauth" CLIENT_ID="C1785e7c046756972f8e8b3dfc2540b7013d6c6a779628c4889ee1bba20b759ee" CLIENT_SECRET="9ccb26cb5b3c8faccf77b12c3d166dca58c69dd8cc4303f633c89f99d9f54ea4" SCOPES="meeting:schedules_read meeting:schedules_write meeting:participants_read meeting:participants_write"  node static.js