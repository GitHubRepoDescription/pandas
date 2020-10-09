""" Google BigQuery support """


def _try_import():
    # since pandas is a dependency of pandas-gbq
    # we need to import on first use
    try:
        import pandas_gbq
    except ImportError:

        # give a nice error message
        raise ImportError("Load data from Google BigQuery\n"
                          "\n"
                          "the pandas-gbq package is not installed\n"
                          "see the docs: https://pandas-gbq.readthedocs.io\n"
                          "\n"
                          "you can install via pip or conda:\n"
                          "pip install pandas-gbq\n"
                          "conda install pandas-gbq -c conda-forge\n")

    return pandas_gbq


def read_gbq(query, project_id=None, index_col=None, col_order=None,
             reauth=False, auth_local_webserver=False, dialect=None,
             location=None, configuration=None, credentials=None,
             use_bqstorage_api=None, private_key=None, verbose=None):
    """
    Load data from Google BigQuery.

    This function requires the `pandas-gbq package
    <https://pandas-gbq.readthedocs.io>`__.

    See the `How to authenticate with Google BigQuery
    <https://pandas-gbq.readthedocs.io/en/latest/howto/authentication.html>`__
    guide for authentication instructions.

    Parameters
    ----------
    query : str
        SQL-Like Query to return data values.
    project_id : str, optional
        Google BigQuery Account project ID. Optional when available from
        the environment.
    index_col : str, optional
        Name of result column to use for index in results DataFrame.
    col_order : list(str), optional
        List of BigQuery column names in the desired order for results
        DataFrame.
    reauth : boolean, default False
        Force Google BigQuery to re-authenticate the user. This is useful
        if multiple accounts are used.
    auth_local_webserver : boolean, default False
        Use the `local webserver flow`_ instead of the `console flow`_
        when getting user credentials.

        .. _local webserver flow:
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_local_server
        .. _console flow:
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_console

        *New in version 0.2.0 of pandas-gbq*.
    dialect : str, default 'legacy'
        Note: The default value is changing to 'standard' in a future verion.

        SQL syntax dialect to use. Value can be one of:

        ``'legacy'``
            Use BigQuery's legacy SQL dialect. For more information see
            `BigQuery Legacy SQL Reference
            <https://cloud.google.com/bigquery/docs/reference/legacy-sql>`__.
        ``'standard'``
            Use BigQuery's standard SQL, which is
            compliant with the SQL 2011 standard. For more information
            see `BigQuery Standard SQL Reference
            <https://cloud.google.com/bigquery/docs/reference/standard-sql/>`__.

        .. versionchanged:: 0.24.0
    location : str, optional
        Location where the query job should run. See the `BigQuery locations
        documentation
        <https://cloud.google.com/bigquery/docs/dataset-locations>`__ for a
        list of available locations. The location must match that of any
        datasets used in the query.

        *New in version 0.5.0 of pandas-gbq*.
    configuration : dict, optional
        Query config parameters for job processing.
        For example:

            configuration = {'query': {'useQueryCache': False}}

        For more information see `BigQuery REST API Reference
        <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query>`__.
    credentials : google.auth.credentials.Credentials, optional
        Credentials for accessing Google APIs. Use this parameter to override
        default credentials, such as to use Compute Engine
        :class:`google.auth.compute_engine.Credentials` or Service Account
        :class:`google.oauth2.service_account.Credentials` directly.

        *New in version 0.8.0 of pandas-gbq*.

        .. versionadded:: 0.24.0
    use_bqstorage_api : bool, default False
        Use the `BigQuery Storage API
        <https://cloud.google.com/bigquery/docs/reference/storage/>`__ to
        download query results quickly, but at an increased cost. To use this
        API, first `enable it in the Cloud Console
        <https://console.cloud.google.com/apis/library/bigquerystorage.googleapis.com>`__.
        You must also have the `bigquery.readsessions.create
        <https://cloud.google.com/bigquery/docs/access-control#roles>`__
        permission on the project you are billing queries to.

        This feature requires version 0.10.0 or later of the ``pandas-gbq``
        package. It also requires the ``google-cloud-bigquery-storage`` and
        ``fastavro`` packages.

        .. versionadded:: 0.25.0
    private_key : str, deprecated
        Deprecated in pandas-gbq version 0.8.0. Use the ``credentials``
        parameter and
        :func:`google.oauth2.service_account.Credentials.from_service_account_info`
        or
        :func:`google.oauth2.service_account.Credentials.from_service_account_file`
        instead.

        Service account private key in JSON format. Can be file path
        or string contents. This is useful for remote server
        authentication (eg. Jupyter/IPython notebook on remote host).
    verbose : None, deprecated
        Deprecated in pandas-gbq version 0.4.0. Use the `logging module to
        adjust verbosity instead
        <https://pandas-gbq.readthedocs.io/en/latest/intro.html#logging>`__.

    Returns
    -------
    df: DataFrame
        DataFrame representing results of query.

    See Also
    --------
    pandas_gbq.read_gbq : This function in the pandas-gbq library.
    DataFrame.to_gbq : Write a DataFrame to Google BigQuery.
    """
    pandas_gbq = _try_import()

    kwargs = {}

    # START: new kwargs.  Don't populate unless explicitly set.
    if use_bqstorage_api is not None:
        kwargs["use_bqstorage_api"] = use_bqstorage_api
    # END: new kwargs

    # START: deprecated kwargs.  Don't populate unless explicitly set.
    if verbose is not None:
        kwargs["verbose"] = verbose

    if private_key is not None:
        kwargs["private_key"] = private_key
    # END: deprecated kwargs

    return pandas_gbq.read_gbq(
        query, project_id=project_id, index_col=index_col,
        col_order=col_order, reauth=reauth,
        auth_local_webserver=auth_local_webserver, dialect=dialect,
        location=location, configuration=configuration,
        credentials=credentials, **kwargs)


def to_gbq(dataframe, destination_table, project_id=None, chunksize=None,
           reauth=False, if_exists='fail', auth_local_webserver=False,
           table_schema=None, location=None, progress_bar=True,
           credentials=None, verbose=None, private_key=None):
    pandas_gbq = _try_import()
    pandas_gbq.to_gbq(dataframe, destination_table, project_id=project_id,
                      chunksize=chunksize, reauth=reauth, if_exists=if_exists,
                      auth_local_webserver=auth_local_webserver,
                      table_schema=table_schema, location=location,
                      progress_bar=progress_bar, credentials=credentials,
                      verbose=verbose, private_key=private_key)