from elasticsearch import Elasticsearch

es = Elasticsearch(
	'https://localhost:9200',
	basic_auth=('elastic', 'elastic'),
	verify_certs=False
)

es_search_numbers = es.search(
  index='numbers',
  query={'match_all': {}}
)['hits']['hits']

es_numbers_numbers = list(set(
  [record['_source']['Number'] for record in es_search_numbers]
))

for number in es_numbers_numbers:
  produce_timestamp = [
    record['_source']['When']
    for record in es_search_numbers
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'produce'
  ]
  if not produce_timestamp:
    continue
  processed_timestamp = [
    record['_source']['When']
    for record in es_search_numbers
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'processed'
  ]
  if not processed_timestamp:
    continue
  processing_time = (
          next(iter(processed_timestamp)) - next(iter(produce_timestamp))
  )
  archived_timestamp = [
    record['_source']['When']
    for record in es_search_numbers
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'archived'
  ]
  if not archived_timestamp:
    continue
  archiving_time = (
          next(iter(archived_timestamp)) - next(iter(processed_timestamp))
  )
  total_time = processing_time + archiving_time
  print(
    f'Number: {number}\t\t'
    f'Processing time: {processing_time}\t'
    f'Archiving time: {archiving_time}\t'
    f'Total time: {total_time}'
  )

es_search_dots = es.search(
  index='dots',
  query={'match_all': {}}
)['hits']['hits']

es_numbers_dots = list(set(
  [record['_source']['Number'] for record in es_search_dots]
))

for number in es_numbers_dots:
  produce_timestamp = [
    record['_source']['When']
    for record in es_search_dots
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'produce'
  ]
  if not produce_timestamp:
    continue
  processed_timestamp = [
    record['_source']['When']
    for record in es_search_dots
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'processed'
  ]
  if not processed_timestamp:
    continue
  processing_time = (
          next(iter(processed_timestamp)) - next(iter(produce_timestamp))
  )
  archived_timestamp = [
    record['_source']['When']
    for record in es_search_dots
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'archived'
  ]
  if not archived_timestamp:
    continue
  archiving_time = (
          next(iter(archived_timestamp)) - next(iter(processed_timestamp))
  )
  total_time = processing_time + archiving_time
  print(
    f'Number: {number}\t\t'
    f'Processing time: {processing_time}\t'
    f'Archiving time: {archiving_time}\t'
    f'Total time: {total_time}'
  )

es_search_increasing = es.search(
  index='increasing',
  query={'match_all': {}}
)['hits']['hits']

es_increasing_numbers = list(set(
  [record['_source']['Number'] for record in es_search_numbers]
))

for number in es_increasing_numbers:
  produce_timestamp = [
    record['_source']['When']
    for record in es_search_increasing
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'produce'
  ]
  if not produce_timestamp:
    continue
  processed_timestamp = [
    record['_source']['When']
    for record in es_search_increasing
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'processed'
  ]
  if not processed_timestamp:
    continue
  processing_time = (
          next(iter(processed_timestamp)) - next(iter(produce_timestamp))
  )
  archived_timestamp = [
    record['_source']['When']
    for record in es_search_increasing
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'archived'
  ]
  if not archived_timestamp:
    continue
  archiving_time = (
          next(iter(archived_timestamp)) - next(iter(processed_timestamp))
  )
  total_time = processing_time + archiving_time
  print(
    f'Number: {number}\t\t'
    f'Processing time: {processing_time}\t'
    f'Archiving time: {archiving_time}\t'
    f'Total time: {total_time}'
  )

es_search_binary = es.search(
  index='binary',
  query={'match_all': {}}
)['hits']['hits']

es_binary_numbers = list(set(
  [record['_source']['Number'] for record in es_search_binary]
))

for number in es_binary_numbers:
  produce_timestamp = [
    record['_source']['When']
    for record in es_search_binary
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'produce'
  ]
  if not produce_timestamp:
    continue
  processed_timestamp = [
    record['_source']['When']
    for record in es_search_binary
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'processed'
  ]
  if not processed_timestamp:
    continue
  processing_time = (
          next(iter(processed_timestamp)) - next(iter(produce_timestamp))
  )
  archived_timestamp = [
    record['_source']['When']
    for record in es_search_binary
    if record['_source']['Number'] == number
       and record['_source']['What'] == 'archived'
  ]
  if not archived_timestamp:
    continue
  archiving_time = (
          next(iter(archived_timestamp)) - next(iter(processed_timestamp))
  )
  total_time = processing_time + archiving_time
  print(
    f'Number: {number}\t\t'
    f'Processing time: {processing_time}\t'
    f'Archiving time: {archiving_time}\t'
    f'Total time: {total_time}'
  )

es.close()
