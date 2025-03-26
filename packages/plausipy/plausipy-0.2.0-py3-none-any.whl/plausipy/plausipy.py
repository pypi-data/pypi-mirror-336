import json
import logging
import os
import uuid
from datetime import datetime

import requests
import safe_exit

from .info import _print_box, show_tracking_info, show_tracking_required
from .paths import DATA_DIR
from .user import Consent, IDManager, Profile, Settings
from .utils import (
  get_localtion_data,
  get_package_tree,
  get_package_version,
  get_python_data,
  get_system_data,
  get_usage_data,
)

# logger
logger = logging.getLogger(__name__)

# api endpoint
API_ENDPOINT = "https://plausipy.com/api/packages/all/records"

class Record:
  
  @classmethod
  def getUserLocation(cls):
    if not hasattr(cls, "_user_location"):
      cls._user_location = get_localtion_data()
    return cls._user_location
  
  @classmethod
  def getUserUsage(cls):
    if not hasattr(cls, "_user_usage"):
      cls._user_usage = get_usage_data()
    return cls._user_usage
  
  @classmethod
  def getUserSystem(cls):
    if not hasattr(cls, "_user_system"):
      cls._user_system = get_system_data()
    return cls._user_system
  
  @classmethod
  def getUserPython(cls):
    if not hasattr(cls, "_user_python"):
      cls._user_python = get_python_data()
    return cls._user_python

class PlausipyConsent:
  
  def __init__(self, consent: Consent):
    self._consent = consent
    self._asked: bool = False
    self._allowed_once: bool = False
    self._denied_once: bool = False
    
  @property
  def hasBeenAsked(self) -> bool:
    return self._asked
  
  def asked(self, value: bool = True):
    self._asked = value
  
  def allowOnce(self):
    self._allowed_once = True
    
  def denyOnce(self):
    self._denied_once = True
  
  @property
  def granted(self) -> bool:
    return ( self._consent == Consent.ALLOW \
          or self == Consent.ASK and self.hasBeenAsked \
          or self._allowed_once
           ) and not self._denied_once
  
  # make comparable 
  def __eq__(self, other):
    if isinstance(other, Consent):
      return self._consent == other
    elif isinstance(other, PlausipyConsent):
      return self._consent == other._consent
    elif isinstance(other, str) and other in [c.value for c in Consent]:
      return self._consent.value == other
    return NotImplemented

class Plausipy:
  
  _id = str(uuid.uuid4())
  _pps: list = []
  _termination_event_registered = False
 
  @classmethod
  def registerTerminationEvent(cls, key: str):
    """
    Register safe exit once
    """

    # check if already registered
    if cls._termination_event_registered:
      logger.info("Termination event already registered.")
      return
    
    # register
    safe_exit.register(cls.terminate)
    cls._termination_event_registered = True
      
  @classmethod  
  def terminate(cls):
    """
    Indicate to plausipy that the trackable execution has ended.
    This usually meand that the program is terminated.
    """
    
    # TODO: maybe disabled on class level makes more sense when it's a user input, however, we also want
    #       to allow disabling tracking on a package level while dependency tracking is still active.
    
    #  log
    logger.info("Terminating plausipy")
    
    # terminate silently if no plausipy instances are running or all are disabled
    if not any([pp.allowed for pp in cls._pps]):
      logger.info("No plausipy instances to terminate")
      return
    
    # stop all plausipy instances that are not already stopped
    for pp in cls._pps:
      if pp._started_on and not pp._ended_on:
        pp.stop()
        
    # print data
    if "PLAUSIPY_DEBUG" in os.environ:
      print("\033[90m", end="")
      _print_box("Plausipy", json.dumps(cls.json(), indent=2))
      print("\033[0m", end="")
        
    # store data
    cls.store()
        
    # send data
    cls.send()
  
  @classmethod
  def json(cls) -> dict:
    """
    Get the data in a json format
    """
        
    # gather general information
    granted_profile = Profile.USER
    consented = True
    
    return {
      "uuid": cls._id,
      "ppy": {
        "version": get_package_version("plausipy"),
      },
      "user": {
        "profile": granted_profile.name,
        "consented": consented,
        "location": Record.getUserLocation(),
        "system": Record.getUserSystem(),
        "python": Record.getUserPython(),
        "timestamp": datetime.now().isoformat(),
      },
      "app": [pp._app_json() for pp in cls._pps if pp.allowed],
    }
   
  @classmethod
  def store(cls):
    """
    Store the data in a file
    """
    
    # get data
    data = cls.json()
    
    # get directory
    file = DATA_DIR / f"{cls._id}.json"
    
    # ensure file exists
    file.parent.mkdir(parents=True, exist_ok=True)
    
    # write data
    with open(file, "w") as f:
      json.dump(data, f)
      
  @classmethod
  def send(cls):
    """
    Send the data to the server
    """
    
    # get data
    data = cls.json()
        
    # check if data is empty
    if not data["app"]:
      logger.info("No application data to send")
      return
        
    # make request
    logger.info("Sending data to server")
    logger.info(json.dumps(data, indent=2))
    
    # get key from main package
    main_package = cls.getMainPackage()
    key = main_package._app_key if main_package else cls._pps[0]._app_key if cls._pps else None

    if not key:
      logger.error("No key found")
      return
    
    # prepare header
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {key}",
      "Accept": "application/json",
      "User-Agent": "plausipy",
    }
    
    # send data
    response = requests.post(API_ENDPOINT, json=data, headers=headers, timeout=5)
    
    # check response
    if response.status_code == 200:
      logger.info("Data sent successfully")
    else:
      logger.error("Data could not be sent: %s", response.text)

  @classmethod    
  def setMainPackage(cls, pp: 'Plausipy'):
    """
    Set the main package
    """
    assert pp in cls._pps, "Package not found"
    assert cls.getMainPackage() is None, "Main package already set"
    pp._is_main = True
    
  @classmethod    
  def getMainPackage(cls) -> 'Plausipy | None':
    """
    Get the main package
    """
    assert sum([pp._is_main for pp in cls._pps]) <= 1, "Multiple main packages found"
    return next((pp for pp in cls._pps if pp._is_main), None)
    
  @classmethod
  def hasMainPackage(cls) -> bool:
    """
    Check if a main package has been set
    """
    return any([pp._is_main for pp in cls._pps])
    
  @classmethod
  def askForConsent(cls):
    """
    Ask for consent
    """
    
    # get all non-disabled packages
    pps = [pp for pp in cls._pps if not pp.disabled]
        
    # get all packages requesting consent
    packages = [pp for pp in pps if pp._consented is None]
    
    # find the main package by key
    package = cls.getMainPackage()
    assert package, "Main package not found"
    
    # determine if we shall ask for consent
    # NOTE: interrupting execution of the program is not pleasant and, in the interest of the user,
    #       must be limited to the required minimum
    ask_for_consent = any([pp.consent == Consent.ASK for pp in pps]) and not package.consent == Consent.DENY
    
    # ask for consent
    if ask_for_consent:
      consent = show_tracking_info(package, packages)
      logger.info("User replied to consent dialogue with: %s", consent)      
      
      if consent == Consent.ALLOW:
        
        # update main package ANY -> ALLOW
        s = Settings.forPackage(package._app_name)      # TODO: harmonize setting update
        s.consent = Consent.ALLOW
        package._consent = PlausipyConsent(s.consent)
        package.consent.asked()
        
        # update all not-main package from ASK -> ALLOW 
        # NOTE: The rationale (which should be subject to further discussion) is to minimize
        #       consent dialogs for users who have already granted consent (to reduce annoyance).
        for pp in [pp for pp in pps if pp.consent == Consent.ASK and pp != package]:
          s = Settings.forPackage(pp._app_name)      # TODO: harmonize setting update
          s.consent = Consent.ALLOW
          pp._consent = PlausipyConsent(s.consent)
          pp.consent.asked()      
          
      elif consent == Consent.DENY:

        # update main package ANY -> DENY
        s = Settings.forPackage(package._app_name)
        s.consent = Consent.DENY
        package._consent = PlausipyConsent(s.consent)
        package.consent.asked()
        
        # set all not-main package to deny once
        # NOTE: The rationale (which should be subject to further discussion) is to avoid permanent
        #       tracking denial for library packages that may be used in various contexts.
        for pp in [pp for pp in pps if pp.consent == Consent.ASK and pp != package]:
          pp.consent.denyOnce()
          pp.consent.asked()
          
      elif consent == Consent.ASK:
        
        # update main package ANY -> ASK
        s = Settings.forPackage(package._app_name)
        s.consent = Consent.ASK
        package._consent = PlausipyConsent(s.consent)
        package.consent.asked()
        
        # mark all not-main package as asked
        for pp in [pp for pp in pps if pp.consent == Consent.ASK and pp != package]:
          pp.consent.asked()          
       
      # print every package and 
      # for pp in pps:
      #   print("Package:", pp._app_name, "Asked:", pp.consent.hasBeenAsked, "Granted:", pp.consent.granted, "Allowed", pp.allowed)
            
    # check if any package has denied tracking where required
    if any([not pp.allowed and pp._require_consent for pp in pps]):
      logger.error("Tracking denied where required")
      allow_once = show_tracking_required([pp._app_name for pp in pps if not pp.allowed and pp._require_consent])
      [pp.consent.allowOnce() for pp in pps if allow_once]
      if any([not pp.allowed and pp._require_consent for pp in pps]):
        exit(1)
    
  def __init__(self, 
      app_name: str, 
      app_key: str, 
      profile: Profile = Profile.PACKAGE, 
      require_consent: bool = False,
      start: bool = False,
      endpoint: str | None = None,
    ):
    
    # log
    logger.info("Initializing plausipy for %s", app_name)
           
    # ptree
    self._ptree = get_package_tree()
    logger.info("Package tree: %s", self._ptree)

    # api endpoint
    if endpoint:
      global API_ENDPOINT
      logger.info("Setting API endpoint to %s", endpoint)
      API_ENDPOINT = endpoint
      
    # register self and terminate event
    self._pps.append(self)
    self.registerTerminationEvent(app_key)    
              
    # app info
    self._is_main = False
    self._id = str(uuid.uuid4())
    self._app_name = app_name
    self._app_key = app_key
    self._require_consent = require_consent
     
    # parameter
    self.disabled = False
    self._consented: bool | None = None
    self._ppy_version = get_package_version("plausipy")
    self._version = get_package_version(self._app_name)
    self._requested_profile = profile
    
    # settings
    settings = Settings.forPackage(self._app_name)
    self._consent = PlausipyConsent(settings.consent)
    self.profile = settings.profile # set granted profile & update track-id # TODO: remove setter

    # ...
    self._returncode = None
    self._started_on = None
    self._ended_on = None
    self._initial_usage = None
    self._memory_delta = None
    self._data = {}

    # start tracking
    if start:
      self.start()
        
  @property
  def id(self) -> str:
    return self._id
  
  @property
  def name(self) -> str:
    return self._app_name
        
  @property    
  def consent(self) -> PlausipyConsent:
    return self._consent
  
  def updateConsent(self, consent: Consent | None = None):
    logger.info("Updating consent from %s to %s for %s", self._consent._consent, consent, self._app_name)
    
    # read from settings
    settings = Settings.forPackage(self._app_name)
    
    # if consent is specified, update settings to new consent value
    # if not, this simply refreshes the consent object from the settings file
    if consent:
      settings.consent = consent
    
    # update consent from settings file
    self._consent = PlausipyConsent(settings.consent)
    
  def start(self):
    """
    Indicate to plausipy that the trackable execution has started.
    This usually means that the program is started.
    """
  
    # start run
    self._started_on = datetime.now()
    
    # capture initial usage
    # NOTE: usage information is collected but won't be captured if tracking has not been consented
    self._initial_usage = get_usage_data()
        
  def stop(self):
    
    # stop
    self._ended_on = datetime.now()
    
    # update usage
    final_usage = get_usage_data()
    memory_delta = final_usage["memory"] - self._initial_usage["memory"]
    self._memory_delta = memory_delta
      
  @property
  def profile(self) -> Profile:
    """
    Get the profile of the current track-id
    """
    return min(self._requested_profile, self._granted_profile)
  
  @profile.setter
  def profile(self, value: Profile):
    """
    Set the granted profile and update the track-id
    NOTE: a granted profile larger than the requested profile has no effect
    """
    self._granted_profile = value
    self._track_id = IDManager().get_id(self.profile, self._app_name)
     
  @property
  def returncode(self) -> int | None:
    """
    Get the return code of the run
    """
    return self._returncode
  
  @returncode.setter
  def returncode(self, value: int):
    """
    Set the return code of the run
    """
    self._returncode = value
     
  @property
  def allowed(self) -> bool:
    return not self.disabled and self.consent.granted
     
  def setData(self, **kwargs):
    """
    Set data for the current run
    """
    self._data.update(kwargs)
     
  def _app_json(self) -> dict:    
    parent_package = self._ptree[2] if len(self._ptree) > 2 else None
    parent_version = get_package_version(parent_package)
    runtime = (self._ended_on - self._started_on).total_seconds() if self._ended_on else 0
    cpu = self._initial_usage["cpu"] if self._initial_usage else None
    
    return {
      "uuid": self._id,
      "name": self._app_name,
      "key": self._app_key,
      "version": self._version,
      "profile": self._requested_profile.name,
      "user": self._track_id.id,
      "parent": parent_package,
      "parent_version": parent_version,
      "returncode": self._returncode,
      "runtime": runtime,
      "cpu": cpu,
      "memory": self._memory_delta,
      "data": self._data,
    }
    
  def __eq__(self, value: 'Plausipy | str'):
    if isinstance(value, Plausipy):
      return self._id == value._id
    elif isinstance(value, str):
      return self._app_name == value
    return NotImplemented