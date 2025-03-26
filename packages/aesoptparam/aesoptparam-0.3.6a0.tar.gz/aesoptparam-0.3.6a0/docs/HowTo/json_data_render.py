# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: aesopt2
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Rendering `dict` and `list` in notebooks 
# This notebook show how to render python `dict`'s and `list`'s in a notebook environment. The `dict` or `list` should serializable as *JSON* as it is how it is done to ensure the data renders correctly. The JSON parser allows `numpy` data types by default.

# %%
import numpy as np

from aesoptparam.utils import display_json_data

# %% [markdown]
# ## Rendering a `dict`

# %%
# Dummy data to render
data = dict(
        a=0.2, 
        b=[0.1, 0.2], 
        c=np.array([0.2, 0.3]), 
        d=dict(
            a=0.1, 
            b=dict(a=0.1)
            ),
        e= [
            dict(a=0.2),
            dict(a=0.3),
            dict(a=[0.1, 0.2, 0.3]),
            dict(a=[dict(a=0.1), 0.5, "str"])
        ]
    )

# %% [markdown]
# ### All closed (*default*)

# %%
display_json_data(data)

# %% [markdown]
# ### All open

# %%
display_json_data(data, True)

# %% [markdown]
# ### Opening some entries
# #### Single entry

# %%
display_json_data(data, fields=["e", 3, "a", 0])

# %% [markdown]
# #### Multiple entries

# %%
display_json_data(data, fields=[["e", 2, "a"], ["e", 3, "a", 0]])

# %% [markdown]
# ### Opening Levels
# Adding `True` at a given level will open all entries at a given level.
#
# #### All at the first level

# %%
display_json_data(data, fields=[True])

# %% [markdown]
# #### All at the first and second level

# %%
display_json_data(data, fields=[True, True])

# %% [markdown]
# #### All at a single entry

# %%
display_json_data(data, fields=["e", True])

# %% [markdown]
# ### Closing some entries
# #### Single entry

# %%
display_json_data(data, True, fields=["e", 3, "a", 0])

# %% [markdown]
# #### Multiple entries

# %%
display_json_data(data, True, fields=[["d", "b"], ["e", 3, "a", 0]])

# %% [markdown]
# ### Closing Levels

# %%
display_json_data(data, True, fields=[5, True])

# %% [markdown]
# ### Rendering large data objects
# When rendering large data object (e. g. data with many arrays) the output can become a large amount of data. To avoid this there is a limit on the array size that will be printed out, which depends on the memory size of the data that is being rendered.
#
# By default it will compute the size of the data and set the `max_arr_size` depending following:
#
# - `max_arr_size = 5` if `size(data) > 1,000,000 bytes` (Rough size of 1000 size 100 arrays)
# - `max_arr_size = 10` if `size(data) > 100,000 bytes` (Rough size of 100 size 100 arrays)
# - `max_arr_size = 100` if `size(data) > 10,000 bytes` (Rough size of 10 size 100 arrays)
# - `max_arr_size = -1` if `size(data) < 10,000 bytes` (Writing all arrays)

# %%
# Initializing dict with large arrays
big_array_dict = {"a"+str(i): np.random.rand(*size) for i, size in enumerate([(5,), (50,), (100,), (1000,), (100, 100), (10, 10, 10)])}

# %%
# Default rendering 
display_json_data(big_array_dict, True)

# %%
# Manually increasing max_arr_size (now rendering the size 50 array)
display_json_data(big_array_dict, True, fields=[["a0"], ["a1"]], max_arr_size=51)

# %%
# Manually decreasing max_arr_size (now rendering not rendering any arrays)
display_json_data(big_array_dict, True, max_arr_size=1)

# %% [markdown]
# ## Rendering `list`

# %%
ldata = [
    0.5,
    "str",
    [0.2, 0.4],
    np.array([0.1, 0.4]),
    dict(
        a=0.1, 
        b=dict(a=0.1)
    ),
    [
        dict(a=[0.1, 0.2, 0.3]),
        dict(a=[dict(a=0.1), 0.5, "str"])
    ]
]

# %% [markdown]
# ### All closed (*default*)

# %%
display_json_data(ldata)

# %% [markdown]
# ### Opening some
# Similar to `dict`. See that for more examples.

# %%
# Open two fields
display_json_data(ldata, fields=[[2], [5, 0, "a"]])

# %%
# Open first two levels for entry 5
display_json_data(ldata, fields=[5, True, True])

# %%
display_json_data(ldata, True, fields=[5])
