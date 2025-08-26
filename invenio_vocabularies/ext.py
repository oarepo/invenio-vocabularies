# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for managing vocabularies."""

from invenio_base.utils import obj_or_import_string

from . import config
from .contrib.affiliations import (
    AffiliationsResource,
    AffiliationsResourceConfig,
    AffiliationsService,
    AffiliationsServiceConfig,
)
from .contrib.awards import (
    AwardsResource,
    AwardsResourceConfig,
    AwardsService,
    AwardsServiceConfig,
)
from .contrib.funders import (
    FundersResource,
    FundersResourceConfig,
    FundersService,
    FundersServiceConfig,
)
from .contrib.names import (
    NamesResource,
    NamesResourceConfig,
    NamesService,
    NamesServiceConfig,
)
from .contrib.subjects import (
    SubjectsResource,
    SubjectsResourceConfig,
    SubjectsService,
    SubjectsServiceConfig,
)
from .resources import (
    VocabulariesAdminResource,
    VocabulariesResource,
    VocabularyTypeResourceConfig,
)
from .services.config import VocabularyTypesServiceConfig
from .services.service import VocabulariesService, VocabularyTypeService


class InvenioVocabularies(object):
    """Invenio-Vocabularies extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.resource = None
        self.service = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resource(app)
        app.extensions["invenio-vocabularies"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("VOCABULARIES_"):
                app.config.setdefault(k, getattr(config, k))

    def service_configs(self, app):
        """Customized service configs."""

        class ServiceConfigs:
            affiliations = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_AFFILIATIONS_SERVICE_CONFIG_CLASS",
                    AffiliationsServiceConfig,
                )
            )
            awards = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_AWARDS_SERVICE_CONFIG_CLASS", AwardsServiceConfig
                )
            )
            funders = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_FUNDERS_SERVICE_CONFIG_CLASS", FundersServiceConfig
                )
            )
            names = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_NAMES_SERVICE_CONFIG_CLASS", NamesServiceConfig
                )
            )
            subjects = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_SUBJECTS_SERVICE_CONFIG_CLASS", SubjectsServiceConfig
                )
            )
            vocabularies = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_SERVICE_CONFIG_CLASS",
                    app.config["VOCABULARIES_SERVICE_CONFIG"],
                )
            )
            vocabulary_types = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_TYPES_SERVICE_CONFIG_CLASS",
                    VocabularyTypesServiceConfig,
                )
            )

        return ServiceConfigs

    def init_services(self, app):
        """Initialize vocabulary resources."""
        service_configs = self.service_configs(app)

        # Services
        self.affiliations_service = obj_or_import_string(
            app.config.get(
                "VOCABULARIES_AFFILIATIONS_SERVICE_CLASS", AffiliationsService
            )
        )(config=service_configs.affiliations)
        self.awards_service = obj_or_import_string(
            app.config.get("VOCABULARIES_AWARDS_SERVICE_CLASS", AwardsService)
        )(config=service_configs.awards)
        self.funders_service = obj_or_import_string(
            app.config.get("VOCABULARIES_FUNDERS_SERVICE_CLASS", FundersService)
        )(config=service_configs.funders)
        self.names_service = obj_or_import_string(
            app.config.get("VOCABULARIES_NAMES_SERVICE_CLASS", NamesService)
        )(config=service_configs.names)
        self.subjects_service = obj_or_import_string(
            app.config.get("VOCABULARIES_SUBJECTS_SERVICE_CLASS", SubjectsService)
        )(config=service_configs.subjects)
        self.vocabularies_service = obj_or_import_string(
            app.config.get("VOCABULARIES_SERVICE_CLASS", VocabulariesService)
        )(config=service_configs.vocabularies)
        self.vocabulary_types_service = obj_or_import_string(
            app.config.get("VOCABULARIES_TYPES_SERVICE_CLASS", VocabularyTypeService)
        )(config=service_configs.vocabulary_types)

    def resource_configs(self, app):
        """Customized resource configs."""

        class ResourceConfigs:
            affiliations = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_AFFILIATIONS_RESOURCE_CONFIG_CLASS",
                    AffiliationsResourceConfig,
                )
            )
            awards = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_AWARDS_RESOURCE_CONFIG_CLASS",
                    AwardsResourceConfig,
                )
            )
            funders = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_FUNDERS_RESOURCE_CONFIG_CLASS",
                    FundersResourceConfig,
                )
            )
            names = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_NAMES_RESOURCE_CONFIG_CLASS", NamesResourceConfig
                )
            )
            subjects = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_SUBJECTS_RESOURCE_CONFIG_CLASS",
                    SubjectsResourceConfig,
                )
            )
            vocabularies = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_RESOURCE_CONFIG_CLASS",
                    app.config["VOCABULARIES_RESOURCE_CONFIG"],
                )
            )
            vocabulary_admin = obj_or_import_string(
                app.config.get(
                    "VOCABULARIES_ADMIN_RESOURCE_CONFIG_CLASS",
                    VocabularyTypeResourceConfig,
                )
            )

        return ResourceConfigs

    def init_resource(self, app):
        """Initialize vocabulary resources."""

        resource_configs = self.resource_configs(app)

        # Generic Vocabularies
        self.affiliations_resource = obj_or_import_string(
            app.config.get(
                "VOCABULARIES_AFFILIATIONS_RESOURCE_CLASS", AffiliationsResource
            )
        )(
            service=self.affiliations_service,
            config=resource_configs.affiliations,
        )

        self.funders_resource = obj_or_import_string(
            app.config.get("VOCABULARIES_FUNDERS_RESOURCE_CLASS", FundersResource)
        )(
            service=self.funders_service,
            config=resource_configs.funders,
        )

        self.names_resource = obj_or_import_string(
            app.config.get("VOCABULARIES_NAMES_RESOURCE_CLASS", NamesResource)
        )(
            service=self.names_service,
            config=resource_configs.names,
        )

        self.awards_resource = obj_or_import_string(
            app.config.get("VOCABULARIES_AWARDS_RESOURCE_CLASS", AwardsResource)
        )(
            service=self.awards_service,
            config=resource_configs.awards,
        )

        self.subjects_resource = obj_or_import_string(
            app.config.get("VOCABULARIES_SUBJECTS_RESOURCE_CLASS", SubjectsResource)
        )(
            service=self.subjects_service,
            config=resource_configs.subjects,
        )

        self.resource = obj_or_import_string(
            app.config.get("VOCABULARIES_RESOURCE_CLASS", VocabulariesResource)
        )(
            service=self.vocabularies_service,
            config=resource_configs.vocabularies,
        )

        self.vocabulary_admin_resource = obj_or_import_string(
            app.config.get(
                "VOCABULARIES_ADMIN_RESOURCE_CLASS", VocabulariesAdminResource
            )
        )(
            service=self.vocabulary_types_service,
            config=resource_configs.vocabulary_admin,
        )


def finalize_app(app):
    """Finalize app.

    NOTE: replace former @record_once decorator
    """
    init(app)


def api_finalize_app(app):
    """Api Finalize app.

    NOTE: replace former @record_once decorator
    """
    init(app)


def init(app):
    """Init app."""
    # Register services - cannot be done in extension because
    # Invenio-Records-Resources might not have been initialized.
    sregistry = app.extensions["invenio-records-resources"].registry
    ext = app.extensions["invenio-vocabularies"]
    sregistry.register(ext.affiliations_service, service_id="affiliations")
    sregistry.register(ext.awards_service, service_id="awards")
    sregistry.register(ext.funders_service, service_id="funders")
    sregistry.register(ext.names_service, service_id="names")
    sregistry.register(ext.subjects_service, service_id="subjects")
    sregistry.register(ext.vocabularies_service, service_id="vocabularies")
    sregistry.register(ext.vocabulary_types_service, service_id="vocabulary-types")
    # Register indexers
    iregistry = app.extensions["invenio-indexer"].registry
    iregistry.register(ext.affiliations_service.indexer, indexer_id="affiliations")
    iregistry.register(ext.awards_service.indexer, indexer_id="awards")
    iregistry.register(ext.funders_service.indexer, indexer_id="funders")
    iregistry.register(ext.names_service.indexer, indexer_id="names")
    iregistry.register(ext.subjects_service.indexer, indexer_id="subjects")
    iregistry.register(ext.vocabularies_service.indexer, indexer_id="vocabularies")
