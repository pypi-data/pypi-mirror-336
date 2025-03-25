.. pipelines


Pipeline Overview
-----------------

A pipeline is organized into :code:`stages`. Each option at the base 
level of a :code:`YAML` file is treated as a "stage". The only required 
stage is :code:`setup`. For more detailed information on stage options 
see :ref:`stages`


:code:`setup` Stage
*******************
Defines the directory structure, high level information like model version 
and the order in which the following :code:`stages` are evaluated.


Output directories
^^^^^^^^^^^^^^^^^^

Output directories are specified relative to the input directory.

.. code-block:: YAML

    setup:

      # defines where the output files for each stage will be written too.
      output_directories:
        monthly: "diags/monthly"
        daily: "diags/daily"
        rtd: "diags/rtd"
        variability: "diags/landon"



.. note::

   If a stage is not present in :code:`output_directories` the variables created in that stage will not be written to disc.


General information
^^^^^^^^^^^^^^^^^^^

.. code-block:: YAML

    setup:
      # general options that may affect how we process yaml->dag
      canesm_version: "6.0"
      file_format: "netcdf4"


Ordering Stages
^^^^^^^^^^^^^^^
This defines the order in which :code:`stages` are executed. For example, we may want to reuse data from the daily stage when
computing the monthly averages, in this case we could write:

.. code-block:: YAML

    setup:
      stages:
        - daily
        - monthly


If no data is reused between stages then this section can be omitted.


Reusing Stages
^^^^^^^^^^^^^^
To reuse results from a previous stage, the `reuse` keyword can be used

.. code-block:: YAML

    setup:
      stages:
        - transforms
        - daily
        - monthly

    transforms:
      variables:
        - GT:
            rename: TS

    daily:
      reuse: transforms
      variables:
        - GT

    monthly:
      reuse: daily
      variables:
        - GT
        - ST


This will tell the :code:`daily` stage to use the variables from the output of 
the :code:`transforms` stage and the :code:`monthly` stage to use the variables from 
the output of the :code:`daily` stage. This will be applied to all variables in 
the stage in this file. Variables that are not defined in prior stages, e.g. :code:`ST` here,
will fallback to earlier stages, in this case the raw data loaded from disc.


Resampling Stages
*****************

Resampling stages take variables and aggregrates them into coarser time bins. Currently the following stages are supported:

 - 3hourly
 - 6hourly
 - daily
 - monthly
 - yearly


.. code-block:: YAML
    
    # compute the monthly mean of `GT` and `ST` variables
    monthly:
      variables:
        - GT
        - ST


Custom Resampling
^^^^^^^^^^^^^^^^^

Additional resampling options can also be applied to all variables in a stage using the :code:`resample` keyword.
If we wanted to do a 3-day average we could use

.. code-block:: YAML

    custom_stage:
      resample: 3D
      variables:
        - ST
        - GT

By default this will peform a mean, but :code:`min`, :code:`max` or :code:`std` are also supported.

.. code-block:: YAML

    custom_stage:
      resample:
        resolution: 3D
        method: std
      variables:
        - ST
        - GT


Cycle Stages
************

Cycling stages take variables and aggregrates them into coarser time bins. Currently the following stages are supported:

 - annual_cycle


.. code-block:: YAML

    # compute the monthly annual cycle of `GT` and `ST` variables
    annual_cycle:
      variables:
        - GT
        - ST


Custom Cycles
^^^^^^^^^^^^^

Additional cycle options can also be applied to all variables in a stage using the :code:`cycle` keyword.
If we wanted to do a daily annual cycle we could use

.. code-block:: YAML

    custom_stage:
      cycle: dayofyear
      variables:
        - ST
        - GT

By default this will peform a mean, but :code:`min`, :code:`max` or :code:`std` are also supported.

.. code-block:: YAML

    custom_stage:
      cycle:
        group: dayofyear
        method: std
      variables:
        - ST
        - GT


:code:`rtd` Stage
*****************
A default RTD stage that converts variables to yearly global average values.

.. code-block:: YAML

    # compute the global, annual mean of `GT` and `ST` variables
    rtd:
      variables:
        - GT
        - ST


Custom Stages
*************
Users can create their own stages. These do not perform any operations by default except saving the ouptut to a file.


.. code-block:: YAML

    # compute monthly standard deviation of the `GT` variable
    variability:
      variables:
        - GT:
            dag:
              dag:
                - name: resampled
                  function: xr.self.resample
                  args: [GT]
                  kwargs:
                    time: MS
                - name: monthly_std
                  function: xr.self.std
                  args: [resampled]
              output: monthly_std


If you would like to call your own functions in a pipeline, see :ref:`custom_functions`.


NetCDF4 Encoding
****************

If you want to write the netcdf files using a particular encoding this can be done at the variable, stage or 
setup level, depending on the scope you would like it to apply. In the example below we specify the default encoding
as :code:`float32` with a :code:`_FillValue` of :code:`1.0e20`. Unless otherwise specified variables will be written
with this encoding (e.g. the daily :code:`ST` variable). The :code:`monthly` stage 
overwrites this and sets a new default, so the monthly variables (e.g. :code:`ST`) will have this encoding. Lastly, if we want a
specific encoding for the monthly, variable, :code:`GT` we can set this at the variable level.

.. code-block:: YAML

    setup:
      ...
      encoding:
        dtype: float32
        _FillValue: 1.0E+20  # note yaml format requires both a "." and a "+" to be read as a float

    monthly:
      reuse: daily
      encoding:
        dtype: float64
        _FillValue: -999
      variables:
        - ST
        - GT:
            encoding: 
              dtype: float64
              _FillValue: 1.0E+20

    daily:
      variables:
        - ST
