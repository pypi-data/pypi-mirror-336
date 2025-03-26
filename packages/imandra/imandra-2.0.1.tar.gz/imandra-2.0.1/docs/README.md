# Imandra CLI and API client library

[Imandra](https://www.imandra.ai) is a cloud-native automated reasoning engine for analysis of algorithms and data.

This package contains the `imandra` Python library for interacting with Imandra's web APIs. It includes:

- `imandra.core`, which provides programmatic access to Imandra X, Imandra's core reasoning engine.
- `imandra.u.agents.*` and `imandra.u.reasoners.*`, bindings to Imandra Universe Agents and Reasoners.
- `imandra.ipl`, tools for analysing Imandra Protocol Language (IPL) files.

If you're interested in developing Imandra X or IPL models, you may also want to see the [Imandra documentation](https://docs.imandra.ai/).

The `imandra` python API reference documentation is available [here](https://docs.imandra.ai/imandra-docs/python/imandra/).

## Authentication

First obtain an API key from https://universe.imandra.ai.

The Python library will read the API key from the first of:

1. The `api_key` parameter passed when instantiating a `Client`.
2. The `IMANDRA_API_KEY` environment variable.
3. The file `$HOME/.config/imandra/api_key` (MacOS and Linux) or `%USERPROFILE%\AppData\Local\imandra\api_key` (Windows)


## Example: Imandra Core

First, ensure dependencies for the `core` module are installed. Note that `imandra.core` requires Python >= 3.12.

```
$ pip install 'imandra[core]'
```

```
$ ipython
...
In [1]: from imandra.core import Client

In [2]: client = Client()

In [3]: client.eval_src('let f x = if x > 0 then if x * x < 0 then x else x + 1 else x')
Out[3]: success: true

In [4]: result = client.verify_src('fun x -> x > 0 ==> f x > 0')

In [5]: result
Out[5]:
proved {
  proof_pp: "..."
}

In [6]: print(result.proved.proof_pp)
{ id = 1; concl = `|- x > 0 ==> f x > 0`;
  view =
  T_deduction {
    premises =
    [("p",
      [{ id = 0; concl = `|- x > 0 ==> f x > 0`;
         view = T_deduction {premises = []} }
        ])
      ]}
  }

In [7]: result = client.instance_src('fun x -> f x = 43')

In [8]: result
Out[8]:
sat {
  model {
    m_type: Instance
    src: "module M = struct\n\n  let x = 42\n\n end\n"
    artifact {
      kind: "cir.model"
      data: "..."
      api_version: "v8"
    }
  }
}

In [9]: print(result.sat.model.src)
module M = struct

  let x = 42

 end

In [10]: result = client.decompose('f')

In [11]: result
Out[11]:
artifact {
  kind: "cir.fun_decomp"
  data: "..."
  api_version: "v8"
}
regions_str {
  constraints_str: "not (x > 0)"
  invariant_str: "x"
  model_str {
    k: "x"
    v: "0"
  }
}
regions_str {
  constraints_str: "not (x * x < 0)"
  constraints_str: "x > 0"
  invariant_str: "x + 1"
  model_str {
    k: "x"
    v: "1"
  }
}
task {
  id {
    id: "task:decomp:rE3VSX-t5kbrrAksQ4saBrMUs2uHTXfu-CqeZunV9aE="
  }
  kind: TASK_DECOMP
}
```

## Example: Imandra Universe reasoners

```
$ pip install imandra
```

```
$ ipython

In [1]: from imandra.u.reasoners.prover9 import Client

In [2]: client = Client()

In [3]: input = "formulas(sos).\n\n  e * x = x.\n  x'\'' * x = e.\n  (x * y) * z = x * (y * z).\n\n  x * x = e.\n\nend_of_list.\n\nformulas(goals).\n\n  x * y = y * x.\n\nend_of_list ...: ."

In [4]: result = client.eval(input)

In [5]: print(result['results'][0])
============================== Prover9 ===============================
Prover9 (64) version 2009-11A, November 2009.
Process 18 was started by universe on localhost,
Mon Jan  6 14:52:26 2025
The command was "/imandra-universe/prover9/bin/prover9 -t 45".
============================== end of head ===========================

============================== INPUT =================================

formulas(sos).
e * x = x.
x''' * x = e.
(x * y) * z = x * (y * z).
x * x = e.
end_of_list.

formulas(goals).
x * y = y * x.
end_of_list.

============================== end of input ==========================

...

============================== PROOF =================================

% Proof 1 at 0.01 (+ 0.00) seconds.
% Length of proof is 16.
% Level of proof is 7.
% Maximum clause weight is 11.000.
% Given clauses 12.

1 x * y = y * x # label(non_clause) # label(goal).  [goal].
2 e * x = x.  [assumption].
3 x''' * x = e.  [assumption].
4 (x * y) * z = x * (y * z).  [assumption].
5 x * x = e.  [assumption].
6 c2 * c1 != c1 * c2.  [deny(1)].
7 x''' * (x * y) = y.  [para(3(a,1),4(a,1,1)),rewrite([2(2)]),flip(a)].
8 x * (x * y) = y.  [para(5(a,1),4(a,1,1)),rewrite([2(2)]),flip(a)].
9 x * (y * (x * y)) = e.  [para(5(a,1),4(a,1)),flip(a)].
11 x'''''' * e = x.  [para(3(a,1),7(a,1,2))].
13 x''' * e = x.  [para(5(a,1),7(a,1,2))].
15 x''' = x.  [back_rewrite(11),rewrite([13(8)])].
16 x * e = x.  [back_rewrite(13),rewrite([15(3)])].
19 x * (y * x) = y.  [para(9(a,1),8(a,1,2)),rewrite([16(2)]),flip(a)].
24 x * y = y * x.  [para(19(a,1),8(a,1,2))].
25 $F.  [resolve(24,a,6,a)].

============================== end of proof ==========================

============================== STATISTICS ============================

Given=12. Generated=122. Kept=23. proofs=1.
Usable=8. Sos=3. Demods=12. Limbo=2, Disabled=14. Hints=0.
Kept_by_rule=0, Deleted_by_rule=0.
Forward_subsumed=99. Back_subsumed=0.
Sos_limit_deleted=0. Sos_displaced=0. Sos_removed=0.
New_demodulators=21 (0 lex), Back_demodulated=9. Back_unit_deleted=0.
Demod_attempts=770. Demod_rewrites=156.
Res_instance_prunes=0. Para_instance_prunes=0. Basic_paramod_prunes=0.
Nonunit_fsub_feature_tests=0. Nonunit_bsub_feature_tests=0.
Megabytes=0.06.
User_CPU=0.01, System_CPU=0.00, Wall_clock=0.

============================== end of statistics =====================

============================== end of search =========================

THEOREM PROVED
```

## Example: Imandra Universe agents

```
$ pip install imandra[universe]
```

```
$ ipython

In [1]: from imandra.u.agents import cogito

In [2]: from langchain_core.messages import HumanMessage

In [3]: g = cogito.get_remote_graph()

In [4]: cogito.create_thread_sync(g)

In [5]: g.invoke({'messages': [HumanMessage(content='hello')], 'tasks': []})
Out[5]:
{'messages': [{'content': "You are Cogito, agent within Imandra Universe - a cloud platform for accessing automated logical reasoners, tools and agents connected to them.",
   'additional_kwargs': {},
   'response_metadata': {},
   'type': 'system',
   'name': None,
   'id': 'ae883182-17df-4ced-87e2-4b79b7777e93'},
  {'content': 'hello',
   'additional_kwargs': {'example': False,
    'additional_kwargs': {},
    'response_metadata': {}},
   'response_metadata': {},
   'type': 'human',
   'name': None,
   'id': 'c5491021-fec5-4e4a-8651-eda927d8e473',
   'example': False},
  {'content': 'Hello! How can I assist you today?',
   'additional_kwargs': {},
   'response_metadata': {},
   'type': 'ai',
   'name': 'supervisor',
   'id': '52e4fd16-235a-4ac2-bdba-3a20d19870a3',
   'example': False,
   'tool_calls': [],
   'invalid_tool_calls': [],
   'usage_metadata': None}],
 'tasks': []}
```

## Example: IPL

```
$ pip install imandra
```

```
$ ipython

In [1]: from imandra.ipl import Client

In [2]: client = Client()

In [3]: job_id = client.unsat_analysis('/path/to/model.ipl')

In [4]: client.status(job_id)
Out[4]: 'processing'

In [5]: client.wait(job_id)
Out[5]: 'done'

In [6]: data = client.data(job_id)

In [7]: print(data['content'].decode('ascii'))
For message flow `simple_orders_one`, unsat cores: []
```

## CLI

The `imandra` package also adds an entry point called `imandra-cli` which exposes the `imandra` library functionality in a more discoverable way:

```sh
$ python3 -m venv ./my/venv
...
$ ./my/venv/pip install imandra
...
$ ./my/venv/bin/imandra-cli --help
usage: imandra [-h] auth,ipl,core,rule-synth,cfb ...

Imandra CLI

positional arguments:
  {auth,ipl,core,rule-synth,cfb}

optional arguments:
  -h, --help            show this help message and exit
```

On Windows, the entry point can be found as `.\my\venv\Scripts\imandra-cli.exe`.

### CLI Authentication

This is the first step to start using the Imandra CLI. Our cloud environment requires a user account, which you can setup like this:

```sh
$ ./my/venv/bin/imandra-cli auth login
```

and follow the prompts to authenticate. This will create the relevant credentials in `~/.imandra` (or `%APPDATA%\imandra` on Windows).

You should now be able to invoke CLI commands that require authentication.
