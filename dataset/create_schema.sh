# The Solr instance must be run at port 8983
# echo 'Create schema for xlore_en'
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"name", "type":"text_general", "multiValued": false}}' http://localhost:8983/solr/xlore_en/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"url", "type":"text_general", "multiValued": false}}' http://localhost:8983/solr/xlore_en/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"article", "type":"text_general", "multiValued": false}}' http://localhost:8983/solr/xlore_en/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"classes", "type":"text_general", "multiValued": true}}' http://localhost:8983/solr/xlore_en/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"properties", "type":"text_general", "multiValued": true}}' http://localhost:8983/solr/xlore_en/schema

# echo 'Create schema for xlore_cn'
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"name", "type":"text_general", "multiValued": false}}' http://localhost:8983/solr/xlore_cn/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"url", "type":"text_general", "multiValued": false}}' http://localhost:8983/solr/xlore_cn/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"article", "type":"text_general", "multiValued": false}}' http://localhost:8983/solr/xlore_cn/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"classes", "type":"text_general", "multiValued": true}}' http://localhost:8983/solr/xlore_cn/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"properties", "type":"text_general", "multiValued": true}}' http://localhost:8983/solr/xlore_cn/schema