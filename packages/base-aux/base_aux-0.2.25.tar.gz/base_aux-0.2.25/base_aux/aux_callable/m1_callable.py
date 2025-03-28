from typing import *
from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_statics.m4_enums import *


# =====================================================================================================================
@final
class CallableAux(NestInit_Source):
    """
    """
    PROCESS_ACTIVE: Enum_ProcessStateActive = Enum_ProcessStateActive.NONE

    def __call__(self, *args, **kwargs) -> Any | NoReturn:
        return self._construct_with_args_kwargs(*args, **kwargs)

    def _construct_with_args_kwargs(self, *args, **kwargs) -> Any | NoReturn:
        """
        unsafe (raise acceptable) get value
        """
        self.PROCESS_ACTIVE = Enum_ProcessStateActive.STARTED

        if callable(self.SOURCE):
            result = self.SOURCE(*args, **kwargs)
        else:
            result = self.SOURCE

        self.PROCESS_ACTIVE = Enum_ProcessStateActive.FINISHED
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self, callable_use: Enum_CallResolve = Enum_CallResolve.RAISE, *args, **kwargs) -> Any | None | Exception | NoReturn | Enum_CallResolve | bool:
        """
        NOTE
        ----
        it is just a collection for all variants in one func!

        it is not so convenient to use param callable_use!
        SO preferred using other/further direct methods!
        """
        if callable_use == Enum_CallResolve.DIRECT:
            return self.SOURCE

        elif callable_use == Enum_CallResolve.EXX:
            return self.resolve_exx(*args, **kwargs)

        elif callable_use == Enum_CallResolve.RAISE:
            return self.resolve_raise(*args, **kwargs)

        elif callable_use == Enum_CallResolve.RAISE_AS_NONE:
            return self.resolve_raise_as_none(*args, **kwargs)

        elif callable_use == Enum_CallResolve.SKIP_CALLABLE:
            return self.resolve_skip_callables(*args, **kwargs)

        elif callable_use == Enum_CallResolve.SKIP_RAISED:
            return self.resolve_skip_raised(*args, **kwargs)

        elif callable_use == Enum_CallResolve.BOOL:
            return self.resolve_bool(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def resolve_exx(self, *args, **kwargs) -> Any | Exception:
        """
        GOAL
        ----
        same as resolve_raise but
        attempt to simplify result by not using try-sentence.
        so if get raise in resolve_raise - return ClsException object

        USEFUL IDEA
        -----------
        1. in gui when its enough to get str() on result and see the result

        SPECIALLY CREATED FOR
        ---------------------
        just in case

        """
        try:
            return self(*args, **kwargs)
        except Exception as exx:
            return exx

    def resolve_raise(self, *args, **kwargs) -> Any | NoReturn:
        """
        just a direct result for call

        SPECIFIC LOGIC
        --------------
        if callable - call and return result.
        else - return source.

        GOAL
        ----
        get common expected for any python code result - simple calculate or raise!
        because of resolve_exx is not enough!

        CREATED SPECIALLY FOR
        ---------------------
        NestGa_Prefix
        """
        return self(*args, **kwargs)

    def resolve_raise_as_none(self, *args, **kwargs) -> Any | None:
        try:
            return self.resolve_raise(*args, **kwargs)
        except:
            return None

    def resolve_skip_callables(self, *args, **kwargs) -> Any | NoReturn:
        if callable(self.SOURCE):
            return Enum_ProcessResult.SKIPPED  # TODO: decide using None ???
        else:
            return self.SOURCE

    def resolve_skip_raised(self, *args, **kwargs) -> Any | NoReturn:
        try:
            return self.resolve_raise(*args, **kwargs)
        except:
            return Enum_ProcessResult.SKIPPED  # TODO: decide using None ???

    def resolve_bool(self, *args, **kwargs) -> bool:
        """
        GOAL
        ----
        same as resolve_exx but
        apply bool func on result

        ability to get bool result with meanings:
            - methods/funcs must be called
                assert get_bool(LAMBDA_TRUE) is True
                assert get_bool(LAMBDA_NONE) is False

            - Exceptions assumed as False
                assert get_bool(Exception) is False
                assert get_bool(Exception("FAIL")) is False
                assert get_bool(LAMBDA_EXX) is False

            - for other values get classic bool()
                assert get_bool(None) is False
                assert get_bool([]) is False
                assert get_bool([None, ]) is True

                assert get_bool(LAMBDA_LIST) is False
                assert get_bool(LAMBDA_LIST, [1, ]) is True

            - if on bool() exception raised - return False!
                assert get_bool(ClsBoolRaise()) is False

        CREATED SPECIALLY FOR
        ---------------------
        funcs.Valid.skip_link or else value/func assumed as bool result
        """
        try:
            result = self.resolve_raise(*args, **kwargs)
            try:
                is_exx = issubclass(result, Exception)  # keep first
            except:
                is_exx = isinstance(result, Exception)

            if is_exx:
                return False
            return bool(result)
        except:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def check_raise(self, *args, **kwargs) -> bool:
        """
        SPECIALLY CREATED FOR
        ---------------------
        check Privates in pytest for skipping

        USE LambdaTrySuccess instead!
        """
        try:
            self.resolve_raise(*args, **kwargs)
            return False
        except:
            return True

    def check_no_raise(self, *args, **kwargs) -> bool:
        return not self.check_raise(*args, **kwargs)


# =====================================================================================================================
