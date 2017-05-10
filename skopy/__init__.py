import numpy
import psycopg2.extensions

psycopg2.extensions.register_adapter(numpy.float64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.uint64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.uint8, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(numpy.int64, psycopg2.extensions.AsIs)
