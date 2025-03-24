from . import html_helper
from . import integrator
from . import base_reporter
from . import tlb_reporter
from . import tax_reporter

# Lazy loading for tax_pres and ins_facts
import importlib

def _import_tax_pres():
    return importlib.import_module('.tax_pres', __package__)

def _import_ins_facts():
    return importlib.import_module('.ins_facts', __package__)

class LazyModule:
    def __init__(self, import_func):
        self._import_func = import_func
        self._module = None
    
    def __getattr__(self, name):
        if self._module is None:
            self._module = self._import_func()
        return getattr(self._module, name)

tax_pres = LazyModule(_import_tax_pres)
ins_facts = LazyModule(_import_ins_facts)

__all__ = [
    'html_helper',
    'integrator',
    'base_reporter',
    'tlb_reporter',
    'tax_reporter',
    'tax_pres',
    'ins_facts'
]