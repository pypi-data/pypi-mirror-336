# -*- coding: utf-8 -*-
# config.py
# Copyright (c) 2025 zedmoster

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Server settings
    server_host: str = Field(default="0.0.0.0", env="REVIT_MCP_HOST")
    server_port: int = Field(default=8080, env="REVIT_MCP_PORT")
    log_level: str = Field(default="INFO", env="REVIT_MCP_LOG_LEVEL")
    
    # Revit connection settings
    revit_host: str = Field(default="localhost", env="REVIT_HOST")
    revit_port: int = Field(default=8080, env="REVIT_PORT")
    connection_timeout: int = Field(default=30, env="REVIT_CONNECTION_TIMEOUT")
    
    # Application settings
    version: str = Field(default="0.2.0")
    debug: bool = Field(default=False, env="REVIT_MCP_DEBUG")
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    @validator("server_port", "revit_port")
    def validate_port(cls, v):
        """Validate port number"""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v
    
    @validator("connection_timeout")
    def validate_timeout(cls, v):
        """Validate connection timeout"""
        if v < 1:
            raise ValueError("Timeout must be positive")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True 