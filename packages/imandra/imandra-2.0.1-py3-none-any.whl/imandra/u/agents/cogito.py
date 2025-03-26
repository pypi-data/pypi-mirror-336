"""
Imandra Universe Cogito Agent.

Example:
    $ pip install 'imandra[universe]'
    $ export IMANDRA_API_KEY=<redacted>
    $ python
    >>> from imandra.u.agents import cogito
    >>> from langchain_core.messages import HumanMessage
    >>> g = cogito.get_remote_graph()
    >>> cogito.create_thread_sync(g)
    >>> response = g.invoke({'messages': [HumanMessage(content='hello')]})
    >>> response['messages'][2]['content']
   'Hello! How can I assist you today?'
"""

import inspect
from typing import Optional

from ... import auth

try:
    from langgraph.pregel.remote import (  # pyright: ignore [reportMissingImports]
        RemoteGraph,
        RunnableConfig,
    )
except ModuleNotFoundError as err:
    note = """
        Install imandra with the optional 'universe' dependency to enable imandra.u.agents.cogito:

            pip install 'imandra[universe]>=2.0.0'
    """
    err.msg += "\n\n" + inspect.cleandoc(note)
    raise


def get_remote_graph(
    config: Optional[RunnableConfig] = None,
    api_key=None,
    scheme=None,
    host=None,
    api_version=None,
) -> RemoteGraph:
    """Create a RemoteGraph configured for Cogito via Imandra Universe."""
    c = auth.Config(api_key=api_key, scheme=scheme, host=host, api_version=api_version)
    url = f"{c.get_url()}/agents/cogito"

    config = config or {}
    config.setdefault("configurable", {}).setdefault("imandra_api_key", api_key)

    remote_graph = RemoteGraph(
        "cogito",
        url=url,
        headers=c.get_headers(),
        config=config,
    )

    return remote_graph


def create_thread_sync(remote_graph: RemoteGraph):
    """Create a thread and configure the RemoteGraph to use it."""
    if remote_graph.sync_client is not None and remote_graph.config is not None:
        thread = remote_graph.sync_client.threads.create()
        remote_graph.config.setdefault("configurable", {})["thread_id"] = thread[
            "thread_id"
        ]
