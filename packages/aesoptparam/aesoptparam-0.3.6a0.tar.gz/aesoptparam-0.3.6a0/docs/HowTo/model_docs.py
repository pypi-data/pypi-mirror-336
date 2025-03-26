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
# # Parametric model documentation
# When building a parametric model using `aesoptparam` it is possible to get a visual representation which include *documentation*, *range*, *units* and *current value* of each of the parameters (this also includes nested `AESOptParameterized`). 
#
# The example below is using the dummy example included in AESOpt Param (`aesoptparam.example`). 
#
# Notice that references (`$ref`), functions (`$function`) and arrays (`numpy.ndarray`) are shown with a simple representations that can be expanded to reveal the full set of values and/or data. Similary nested `AESOptParameterized` instances are also rendered to be expanded when using the `SubParameterized` and/or `ListOfParameterized` parameters. 

# %%
from aesoptparam.example import main

# %% [markdown]
# ## Creating a model instance

# %%
# %% Creating a model instance of 

# Creating an instance of the parametrized object
main_ins = main(i=dict(a=5.0, b=[0.0, 1.0]))

# Adding a dummy 
main_ins.add_sub_list();

# %% [markdown]
# ## Showing documentation
#
# ### Notebook/HTML view (`._repr_html_`)

# %%
main_ins

# %% [markdown]
# Rendering sub1 (`main.sub1`)

# %%
main_ins.sub1

# %% [markdown]
# One can also get a little more control over the rendering using the `.display` method.

# %%
main_ins.display(open=False, title="Another Instance Title", max_arr_size=-1)

# %% [markdown]
# ### Notebook/text (`?`)

# %%
# ?main_ins

# %% [markdown]
# ### Python interperter/Notebook/Text (`help`)

# %%
help(main_ins)
