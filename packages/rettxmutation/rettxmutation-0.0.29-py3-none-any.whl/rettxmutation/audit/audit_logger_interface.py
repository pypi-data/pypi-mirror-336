# rettxmutation/audit/audit_logger_interface.py
from abc import ABC, abstractmethod
from typing import Optional, Dict

class AuditLoggerInterface(ABC):
    @abstractmethod
    def log_event(self, 
                  message: str,
                  correlation_id: str, 
                  group: str, 
                  stage: str, 
                  status: str, 
                  context: Optional[Dict] = None):
        pass
