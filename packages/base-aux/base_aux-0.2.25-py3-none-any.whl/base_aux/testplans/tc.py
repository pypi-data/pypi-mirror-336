import json
import datetime
from PyQt5.QtCore import QThread, pyqtSignal

from base_aux.aux_dict.m3_dict_attr1_simple import *
from base_aux.aux_callable.m1_callable import *
from base_aux.valid.m2_valid_base import *
from base_aux.pyqt.m0_signals import *
from base_aux.loggers.m1_logger import *
from base_aux.base_statics.m4_enums import *

from .tc_types import TYPING__RESULT_BASE, TYPING__RESULT_W_NORETURN, TYPING__RESULT_W_EXX
from .models import *
from base_aux.base_nest_dunders.m6_eq2_cls import *
from base_aux.base_statics.m4_enums import NestEq_Enum


# =====================================================================================================================
class _Base0_TestCase(Logger):
    # just to use in Signals before defining exact
    pass


# =====================================================================================================================
class Enum_TcGroup_Base(NestEq_Enum):
    NONE = None


# =====================================================================================================================
class Signals(SignalsTemplate):
    signal__tc_state_changed = pyqtSignal(_Base0_TestCase)


# =====================================================================================================================
class _Base1_TestCase(Nest_EqCls, _Base0_TestCase, QThread):
    LOG_ENABLE = False
    LOG_USE_FILE = False

    # SETTINGS ------------------------------------
    NAME: str = ""      # set auto!
    DESCRIPTION: str = ""
    SKIP: Optional[bool] = None     # access only over CLASS attribute! not instance!!!
    skip_tc_dut: Optional[bool] = None
    ASYNC: Optional[bool] = True
    # STOP_IF_FALSE_RESULT: Optional[bool] = None     # NOT USED NOW! MAYBE NOT IMPORTANT!!!
    SETTINGS_FILES: Union[None, pathlib.Path, list[pathlib.Path]] = None

    DEVICES__BREEDER_CLS: type['DevicesBreeder'] = None

    # AUXILIARY -----------------------------------
    STATE_ACTIVE__CLS: Enum_ProcessStateActive = Enum_ProcessStateActive.NONE

    signals: Signals = Signals()  # FIXME: need signal ON BASE CLASS! need only one SlotConnection! need Singleton?
    _INSTS_DICT_CLS: dict[type[Any], dict[Any, Any]]

    result__startup_cls: TYPING__RESULT_BASE | Enum_ProcessStateActive = None
    result__teardown_cls: TYPING__RESULT_BASE | Enum_ProcessStateActive = None

    # INSTANCE ------------------------------------
    _inst_inited: Optional[bool] = None

    INDEX: int
    SETTINGS: DictAttr = {}
    DEVICES__BREEDER_INST: 'DevicesBreeder'

    result__startup: TYPING__RESULT_W_EXX = None
    result__teardown: TYPING__RESULT_W_EXX = None

    _result: TYPING__RESULT_W_EXX = None
    _timestamp_last: Optional[datetime.datetime]
    timestamp_start: Optional[datetime.datetime]
    details: dict[str, Any]
    exx: Optional[Exception]
    progress: int

    # =================================================================================================================
    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum:
        """
        GOAL
        ----
        REDEFINE TO USE AS CMP VALUE
        """
        return Enum_TcGroup_Base.NONE

    # =================================================================================================================
    @classmethod
    def devices__apply(cls, devices_cls: type['DevicesBreeder'] = None) -> None:
        if devices_cls is not None:
            cls.DEVICES__BREEDER_CLS = devices_cls
            cls.TCS__LIST.clear()

        if cls.DEVICES__BREEDER_CLS:
            cls.DEVICES__BREEDER_CLS.generate__objects()
            if not cls.TCS__LIST:
                for index in range(cls.DEVICES__BREEDER_CLS.COUNT):
                    tc_inst = cls(index=index)

    @classmethod
    @property
    def TCS__LIST(cls) -> list[Self]:
        try:
            result = list(_Base1_TestCase._INSTS_DICT_CLS[cls].values())
        except:
            result = []
        return result

    # =================================================================================================================
    def __new__(cls, index: int, *args, **kwargs):
        """
        use singletons for every class!
        """
        if not hasattr(_Base1_TestCase, "_INSTS_DICT_CLS"):
            setattr(_Base1_TestCase, "_INSTS_DICT_CLS", {})

        if cls not in _Base1_TestCase._INSTS_DICT_CLS:
            _Base1_TestCase._INSTS_DICT_CLS.update({cls: {}})

        INSTS_DICT = _Base1_TestCase._INSTS_DICT_CLS[cls]

        try:
            INST = INSTS_DICT[index]
        except:
            INST = super().__new__(cls)
            INSTS_DICT[index] = INST

        print(f"{cls.__name__}.__NEW__={index=}/{args=}/{kwargs=}//groups={len(_Base1_TestCase._INSTS_DICT_CLS)}/group={len(INSTS_DICT)}")
        return INST

    def __init__(self, index: int):
        if self._inst_inited:
            return

        # NEW INSTANCE -----------------------------
        self.INDEX = index
        self.clear()
        super().__init__()

        if self.DEVICES__BREEDER_CLS:
            self.DEVICES__BREEDER_INST = self.DEVICES__BREEDER_CLS(index)

        self.SETTINGS = DictAttr(self.settings_read())
        self._inst_inited = True

    # =================================================================================================================
    @property
    def timestamp_last(self) -> datetime.datetime | None:
        """
        None - not even started
        float - was started!
            stable - finished
            UnStable - in progress (active thread)
        """
        if self._timestamp_last:
            return self._timestamp_last

        if self.isRunning():
            return datetime.datetime.now()

    @timestamp_last.setter
    def timestamp_last(self, value: datetime.datetime | None) -> None:
        self._timestamp_last = value

    # =================================================================================================================
    @classmethod
    def settings_read(cls, files: Union[None, pathlib.Path, list[pathlib.Path]] = None) -> dict:
        result = {}

        _settings_files = files or cls.SETTINGS_FILES
        if _settings_files:
            if isinstance(_settings_files, pathlib.Path):
                _settings_files = [_settings_files, ]

            if isinstance(_settings_files, (list, tuple)):
                for file in _settings_files:
                    if file.exists():
                        file_data = json.loads(file.read_text())
                        result.update(file_data)
        return result

    def clear(self) -> None:
        self.result__startup = None
        self.result__teardown = None
        self.result = None

        self.timestamp_last = None
        self.timestamp_start = None

        self.details = {}
        self.exx = None
        self.progress = 0

    @classmethod
    def clear__cls(cls):
        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.NONE
        cls.result__startup_cls = None
        cls.result__teardown_cls = None
        for tc in cls.TCS__LIST:
            tc.clear()

    # @classmethod
    # @property
    # def NAME(cls):
    #     return cls.__name__
    #     # return pathlib.Path(__file__).name    # work as last destination where property starts!

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> TYPING__RESULT_W_EXX:
        return self._result

    @result.setter
    def result(self, value: TYPING__RESULT_W_EXX) -> None:
        self._result = value
        self.signals.signal__tc_state_changed.emit(self)

    # # ---------------------------------------------------------
    # @classmethod
    # @property
    # def result__startup_cls(cls) -> Optional[bool]:
    #     return cls.__result__cls_startup
    #
    # @classmethod
    # @result__startup_cls.setter
    # def result__startup_cls(cls, value: Optional[bool]) -> None:
    #     cls.__result__cls_startup = value
    #     # cls.signals.signal__tc_state_changed.emit(cls)

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: dict[str, Any]) -> None:
        self.LOGGER.debug("")
        self.details.update(details)
        # self.signals.signal__tc_state_changed.emit(self)

    # =================================================================================================================
    @classmethod
    def run__cls(cls, cls_prev: type[Self] | None = None, cls_next: type[Self] | None = None) -> None | bool:
        """run TC on batch duts(??? may be INDEXES???)
        prefered using in thread on upper level!

        :param cls_prev: use for apply group in sequence
        :return:
            NONE - if SKIP for any reason
            True - need continue TP
            False - cant continue! need stop TP
        """
        # if not cls.DEVICES__BREEDER_CLS.LIST__DUT:
        #     return

        print(f"run__cls=START={cls.NAME=}={'=' * 50}")

        # SKIP ---------------------------------------------------
        # if cls.SKIP:
        #     print(f"run__cls=SKIP={cls.NAME=}={'=' * 50}")
        #     return

        cls.clear__cls()

        # STARTUP ----------------------------------------
        if cls_prev and Nest_EqCls._eq_classes__check(cls, cls_prev):
            cls.result__startup_cls = cls_prev.result__startup_cls
        else:
            cls.result__startup_cls = cls.startup__cls()

        # WORK ---------------------------------------------------
        if cls.result__startup_cls:
            # BATCH --------------------------
            for tc_inst in cls.TCS__LIST:
                if tc_inst.skip_tc_dut:
                    continue

                print(f"run__cls=tc_inst.start({tc_inst.INDEX=})")
                tc_inst.start()
                if not cls.ASYNC:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inONEBYONE")
                    tc_inst.wait()

            # WAIT --------------------------
            if cls.ASYNC:
                for tc_inst in cls.TCS__LIST:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inPARALLEL")
                    tc_inst.wait()

        # TERDOWN ----------------------------------------
        if cls_next and Nest_EqCls._eq_classes__check(cls, cls_next):
            pass
        else:
            cls.result__teardown_cls = cls.teardown__cls()

        # FINISH -------------------------------------------------
        print(f"[TC]FINISH={cls.NAME=}={'=' * 50}")
        if cls.result__startup_cls and cls.result__teardown_cls is False:
            return False
        else:
            return True

    def run(self) -> None:
        self.LOGGER.debug("run")

        # PREPARE --------
        self.clear()
        self.timestamp_start = datetime.datetime.now()
        if (
                not hasattr(self.DEVICES__BREEDER_INST, "DUT")
                or
                self.DEVICES__BREEDER_INST.DUT.SKIP
                or
                not self.DEVICES__BREEDER_INST.DUT.DEV_FOUND
                or
                not self.DEVICES__BREEDER_INST.DUT.connect()
        ):
            return

        # WORK --------
        self.LOGGER.debug("run-startup")
        if self.startup():
            try:
                self.LOGGER.debug("run-run_wrapped START")
                self.result = self.run__wrapped()
                if isinstance(self.result, Valid):
                    self.result.run__if_not_finished()

                self.LOGGER.debug(f"run-run_wrapped FINISHED WITH {self.result=}")
            except Exception as exx:
                self.result = False
                self.exx = exx
        self.LOGGER.debug("run-teardown")
        self.teardown()

    # STARTUP/TEARDOWN ------------------------------------------------------------------------------------------------
    @classmethod
    def startup__cls(cls) -> TYPING__RESULT_W_EXX:
        """before batch work
        """
        print(f"startup__cls")
        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.STARTED
        cls.result__startup_cls = Enum_ProcessStateActive.STARTED
        # cls.clear__cls()

        result = cls.startup__cls__wrapped
        result = CallableAux(result).resolve_exx()
        if isinstance(result, Valid):
            result.run__if_not_finished()
        print(f"{cls.result__startup_cls=}")
        cls.result__startup_cls = result
        return result

    def startup(self) -> TYPING__RESULT_W_EXX:
        self.LOGGER.debug("")
        self.progress = 1

        result = self.startup__wrapped
        result = CallableAux(result).resolve_exx()
        if isinstance(result, Valid):
            result.run__if_not_finished()
        self.result__startup = result
        return result

    def teardown(self) -> TYPING__RESULT_W_EXX:
        self.LOGGER.debug("")
        self.timestamp_last = datetime.datetime.now()
        self.progress = 99

        result = self.teardown__wrapped
        result = CallableAux(result).resolve_exx()
        if isinstance(result, Valid):
            result.run__if_not_finished()

        self.progress = 100
        self.result__teardown = result
        return result

    @classmethod
    def teardown__cls(cls) -> TYPING__RESULT_W_EXX:
        print(f"run__cls=teardown__cls")

        if cls.STATE_ACTIVE__CLS == Enum_ProcessStateActive.STARTED:
            cls.result__teardown_cls = Enum_ProcessStateActive.STARTED

            result = cls.teardown__cls__wrapped
            result = CallableAux(result).resolve_exx()
            if isinstance(result, Valid):
                result.run__if_not_finished()
            cls.result__teardown_cls = result

            if not result:
                print(f"[FAIL]{cls.result__teardown_cls=}//{cls.NAME}")

        else:
            result = cls.result__teardown_cls

        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.FINISHED
        return result

    # =================================================================================================================
    @classmethod
    def terminate__cls(cls) -> None:
        for tc_inst in cls.TCS__LIST:
            try:
                if tc_inst.isRunning() and not tc_inst.isFinished():
                    tc_inst.terminate()
            except:
                pass

        cls.teardown__cls()

    def terminate(self) -> None:
        self.LOGGER.debug("")

        super().terminate()

        progress = self.progress
        self.teardown()
        self.progress = progress

    # REDEFINE ========================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        return True

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True

    def run__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True

    def teardown__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        print("HELLO")
        return True


# =====================================================================================================================
class _Info(_Base1_TestCase):
    """
    separated class for gen results/info by models!
    """
    INFO_STR__ADD_ATTRS: Iterable[str] = []

    @classmethod
    def get__info__tc(cls) -> dict[str, Any]:
        """
        get info/structure about TcCls
        """
        result = {
            "TC_NAME": cls.NAME,
            "TC_DESCRIPTION": cls.DESCRIPTION,
            "TC_ASYNC": cls.ASYNC,
            "TC_SKIP": cls.SKIP,
            "TC_SETTINGS": cls.settings_read(),
        }
        return result

    # =================================================================================================================
    def get__results_pretty(self) -> str:
        # FIXME: GET FROM INFO_GET????
        result = ""

        result += f"DUT_INDEX={self.INDEX}\n"
        result += f"DUT_SN={self.DEVICES__BREEDER_INST.DUT.SN}\n"
        result += f"DUT_ADDRESS={self.DEVICES__BREEDER_INST.DUT.ADDRESS}\n"
        result += f"tc_skip_dut={self.skip_tc_dut}\n"

        result += f"TC_NAME={self.NAME}\n"
        result += f"TC_GROUP={self._EQ_CLS__VALUE}\n"
        result += f"TC_DESCRIPTION={self.DESCRIPTION}\n"
        result += f"TC_ASYNC={self.ASYNC}\n"
        result += f"TC_SKIP={self.SKIP}\n"

        result += f"SETTINGS=====================\n"
        if self.SETTINGS:
            for name, value in self.SETTINGS.items():
                result += f"{name}:{value}\n"

        result += f"INFO_STR__ADD_ATTRS===========\n"
        if self.INFO_STR__ADD_ATTRS:
            for name in self.INFO_STR__ADD_ATTRS:
                if hasattr(self, name):
                    result += f"{name}:{getattr(self, name)}\n"

        result += f"PROGRESS=====================\n"
        result += f"timestamp_start={self.timestamp_start}\n"
        result += f"timestamp_last={self.timestamp_last}\n"
        result += f"progress={self.progress}\n"
        result += f"exx={self.exx}\n"

        result += "-"*60 + "\n"
        result += f"result__startup={self.result__startup}\n"
        result += "-"*60 + "\n"
        result += f"result={self.result}\n"
        result += "-"*60 + "\n"
        result += f"result__teardown={self.result__teardown}\n"
        result += "-"*60 + "\n"

        result += f"DETAILS=====================\n"
        for name, value in self.details.items():
            result += f"{name}={value}\n"
        return result

    # =================================================================================================================
    def get__results(self, add_info_dut: bool = True, add_info_tc: bool = True) -> dict[str, Any]:
        self.LOGGER.debug("")

        info_dut = {}
        try:
            if add_info_dut:
                info_dut = self.DEVICES__BREEDER_INST.DUT.get__info__dev()
        except:
            pass

        info_tc = {}
        if add_info_tc:
            info_tc = self.get__info__tc()

        result = {
            **info_tc,
            **info_dut,

            # RESULTS
            "timestamp_start": self.timestamp_start and str(self.timestamp_start),
            "tc_active": self.isRunning(),
            "tc_progress": self.progress,
            "tc_result_startup": bool(self.result__startup),
            "tc_result": None if self.result is None else bool(self.result),
            "tc_details": self.details,
            "result__teardown": bool(self.result__teardown),
            "timestamp_last": self.timestamp_last and str(self.timestamp_last),
            "log": self.get__results_pretty(),
        }
        return result

    @classmethod
    def get__results__all(cls) -> dict[int, dict[str, Any]]:
        results = {}
        for tc_inst in cls.TCS__LIST:
            results.update({tc_inst.INDEX: tc_inst.get__results()})
        return results


class Base_TestCase(_Info):
    """
    """


# =====================================================================================================================
