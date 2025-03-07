In the short term I need to implement concurrent test.

Streamline log structure to collect and interpret data.

I need to make sure that I am collecting the following variables for future benchmark:
- "innodb_" variables
- max_connections
- wait_timeout
- thread_cache_size
- key_buffer_size
- tmp_table_size

In the long term I need to simplify the generator and benchmark interface to make sure that
end user does not have to keep track of underlying requirements.
