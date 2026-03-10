
## Design a Toolchain/SDKs to FindSDK subclassing


### Example Code

Subclassing a FindSDK class implementation can follow with this completion example:
```

from . import FindSDK
from typing import Any, Literal, Union, overload
from utils import *



class FindMySDK(FindSDK):
    
    name  = ...
    props = ...
    FOO = ...
    BAR = ...

    def __init__(self, ...):
        super().__init__()

        self.info: dict[
            Literal["foo", "bar", "AMD", ...],
            Any
        ]

        self._foo_X = ...
        self._foo_Y = ...
        ...

        self.dispatch_map = {
            "post_foo": self._post_foo,
            "post_bar": self._post_bar,
            ...
        }

    def __repr__(self):
        ...

    @property
    def foo(self):
        return self.info["foo"]

    @property
    def bar(self):
        return self.info["bar"]

    def __WINDOWS__(self):        
        # If device is Windows, __init__() will do this function to self.info
        # self.__WINDOWS__() -> self.info at FindSDK.__init__()

        ...

        return {
            "foo": foo,
            "bar": bar,
            ...
        }

    def __LINUX__(self):
        # If device is Linux, __init__() will do this function to self.info
        # self.__LINUX__() -> self.info at FindSDK.__init__()
        
        ...

        return {
            "foo": foo,
            "bar": bar,
            ...
        }

    def __BSD__(self):
        # If device is BSD type, __init__() will do this function to self.info
        # self.__BSD__() -> self.info at FindSDK.__init__()
        
        ...

        return {
            "foo": foo,
            "bar": bar,
            ...
        }

    # =============================================================

    def _find_foo(self, ...): 
        ...

    def _find_bar(self, ...): 
        ...

    def _amd_red_team(self, ...):
        ...

    # =============================================================

    @overload
    def post(self,
             kwd:Literal["foo"]="foo",
             condition:Literal["REQUIRED", "OPTIONAL"]="REQUIRED",
             /,
             *,
             param1: ...
             param2: ...,
             ...,
             fail_level:Literal["FATAL", "WARNING", "HINT"]="FATAL"): ...
    @overload
    def post(self,
             kwd:Literal["bar"]="bar",
             condition:Literal["REQUIRED", "OPTIONAL"]="REQUIRED",
             /,
             *,
             param1: ...,
             param2: ...,
             ...,
             fail_level:Literal["FATAL", "WARNING", "HINT"]="FATAL"): ...

    def post(self, kwd:str, condition:str, **kwargs:Any)
        return super().post(kwd, condition, **kwargs)

    # ================================================================

    def _post_foo(self, 
                  *, 
                  param1: ..., 
                  param2: ...,, 
                  ..., 
                  condition:Literal["REQUIRED", "OPTIONAL"]="", 
                  fail_level:Literal["FATAL", "WARNING", "HINT"]="FATAL"):
        
        # Do some logic tricks
        ... 

        # Result write #1
        result = SUCCESS if <CONDITION> ... else self._compoment_fail(condition, fail_level)
        # Result write #2
        result = self._compoment_fail(condition, fail_level) if not <CONDITION> ... else SUCCESS

        if result is not SUCCESS:
            print(cstring("Failed reason", result))

        return SUCCESS or HINT or WARNING or FATAL

    def _post_bar(self, 
                  *, 
                  param1: ..., 
                  param2: ...,, 
                  ..., 
                  condition:Literal["REQUIRED", "OPTIONAL"]="", 
                  fail_level:Literal["FATAL", "WARNING", "HINT"]="FATAL"):

        ...

```

## Notes

Some functions have special use:

1. Initialize method `__init__()`

    A FindSDK subclassing should have FindSDK behavior inheritance, to generate this SDK's information `self.info` from [OS dunderscore method](#notes/2.).

    `self.info` can be type hinted for desining with intellisense.

    Also, `__init__()` need to implement its post dispatch map `self._dispatch_map` dict object, to define which post function 
    need to be called when SDK is established and have been called for testing.

    ```
    def __init__(self):
        super().__init__()

        self.info: dict[
            Literal["foo", "bar", "AMD", ...],
            Any
        ]

        self._dispatch_map = {
            "foo": self._post_foo,
            "bar": self._post_bar,
            ...
        }
    ```


2. OS dunderscore `__<OS_TYPE>__()`:

    The behavior will run on `<OS_TYPE>` platform.

    | Operating System | dunderscore |
    | :---:     | :---: |
    | Windows   | `__WINDOWS__()` |
    | Linux     | `__LINUX__()` |
    | BSD based | `__BSD__()` |
    | macOS     | `__MACOS__()` |


    Any information in initialization caculated need return via OS dunderscore. It requires to returns a dict object to `self.info`, which this method is inherited from `FindSDK` class. 

    The `__BSD__()` and `__MACOS__()` method will change its implementation since will haver future support or deprecation.

    ```
    def __WINDOWS__(self):
        ...


        return {
            "foo": ...
            "bar": ...
        }
    ```

3. `__repr__()`

    At default, `__repr__()` will print formatted info message with `f"{self.Version} -- {self.exe}"`.

    Change its print status can just overwrite it.

4. `_dispatch_map`: 

    As [`__init__()`](#notes/1.) metioned, this specialized dict records related post functions (as a phone book). 

    Which its key-value pairs should be `kwd - function_name` like:
    ```
    {
        "AVAIL":    self._post_amdgpu_avail,
        "REDTEAM"   self._post_join_the_redteam,
    }
    ```
    Please to avoid functions is called:
    ```
    # This is a invalid setting
    # Do not make values with ()
    {
        "AVAIL":    self._post_amdgpu_avail(),
        "REDTEAM"   self._post_join_the_redteam(),
    }
    ```

5. `_find_<what>` and underscored functions

    The `FindSDK` class have implemented `_find_program` and `_find_version` function for required executable/program finding and its version grepping.

    ```
    exe = self._find_program("amd-smi")
    ver = self._find_version(exe, args="--version", vertemp="X.Y.Z")
    ```

    If a specified functions is need, we can design it as underscored functions like `_find_foo`, `_function_bar` etc.

6. properties

    Properties can be defined via `@properties` decorator.

    For convinence, properties can get from `self.info`.

    ```
    @property
    def FOO(self):
        return self.info["foo"]
    ```

    Property `exe` and `Version` are fixed as constant property.


7. `_post_<what>` functions

    The core of SDK testing its features examination.

    Requires return type with `SUCCESS`, `HINT`, `WARNING`, `FATAL` singleton type (This pre-diagnose system only).

    You can manually specify different check status type, or base on your required/optional condition and fail level, use `_compoment_fail()` function
    to deside your failed type `HINT`, `WARNING`, `FATAL`.

    ```
    def _post_foo(self,
                  *,
                  condition:condition:Literal["REQUIRED", "OPTIONAL"]="REQUIRED",
                  fail_level:Literal["HINT", "WARNING", "ERROR"]="ERROR",
                  args1: ...,
                  args2: ...,)
        # Do something check here

        result: SUCCESS | HINT | WARNING | FATAL

        if what:
            result = SUCCESS if what2 else self._compoment_fail(condition, fail_level)
        elif what:
            result = FATAL

        

        if result is not SUCCESS:
            reason = f"""Something is bad with {self.FOO} ..."""

            message = 

        return result
    ```

8. `post()` functions
   
   The opened test function (as the interface) called `post`.

    Make sure do `@overload` for different post option type hint, then do post behavior inheritance.

    This Interface is for writing task check script.
    ```
        @overload
        def post(self, kwd:Literal["foo", "bar"], condition:Literal["REQUIRED", "OPTIONAL"]=..., /, *, fail_level:Literal["HINT", "WARNING", "ERROR"]=..., **kwargs: ...): ...
        @overload
        def post(self, kwd:Literal[...], condition:Literal["REQUIRED", "OPTIONAL"]=..., /, *, fail_level:Literal["HINT", "WARNING", "ERROR"]=..., **kwargs: ...): ...
        @overload
        def post(self, kwd:Literal[...], condition:Literal["REQUIRED", "OPTIONAL"]=..., /, *, fail_level:Literal["HINT", "WARNING", "ERROR"]=..., **kwargs: ...): ...

        ...

        def post(self, kwd:str, condition:str, **kwargs:Any):
            return super().post(kwd, condition=condition, **kwargs)

    ```
