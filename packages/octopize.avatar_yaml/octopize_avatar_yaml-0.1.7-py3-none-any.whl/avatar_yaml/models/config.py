from typing import Any

from avatar_yaml.models.common import Metadata, ModelKind
from avatar_yaml.models.parameters import (
    AlignmentMethod,
    AvatarizationParameters,
    ExcludeVariablesMethod,
    ImputeMethod,
    PrivacyMetricsParameters,
    ProjectionType,
    ReportParameters,
    ReportParametersSpec,
    Results,
    SignalMetricsParameters,
    TimeSeriesParameters,
    get_avatarization_parameters,
    get_privacy_metrics_parameters,
    get_signal_metrics_parameters,
)
from avatar_yaml.models.schema import (
    ColumnInfo,
    ColumnType,
    Schema,
    TableDataInfo,
    TableInfo,
    TableLinkInfo,
    TableLinkInfoSpec,
    get_schema,
)
from avatar_yaml.models.volume import Volume, VolumeSpec
from avatar_yaml.yaml_utils import aggregate_yamls, to_yaml
from pydantic import BaseModel


class Config(BaseModel):
    set_name: str
    volume: Volume | None = None
    results_volume: Volume | None = None
    original_schema: Schema | None = None
    avatar_schema: Schema | None = None
    tables: dict[str, TableInfo] = {}
    avatar_tables: dict[str, TableInfo] = {}
    avatarization: dict[str, AvatarizationParameters] = {}
    time_series: dict[str, TimeSeriesParameters] = {}
    privacy_metrics: dict[str, PrivacyMetricsParameters] = {}
    signal_metrics: dict[str, SignalMetricsParameters] = {}
    report: ReportParameters | None = None
    seed: int | None = None

    def _schema_name(self):
        return (
            self.original_schema.metadata.name
            if self.original_schema and self.original_schema.metadata.name
            else self.set_name
        )

    def _avatar_schema_name(self):
        return (
            self.avatar_schema.metadata.name
            if self.avatar_schema and self.original_schema.metadata.name
            else self.set_name + "_avatarized"
        )

    def create_schema(self, name: str, tables: list[TableInfo] | None = None):
        if tables is None:
            tables = list(self.tables.values())
        self.original_schema = get_schema(name, tables)

    def create_avatar_schema(
        self, name: str, schema_ref: str, tables: list[TableInfo] | None = None
    ):
        if schema_ref is not self._schema_name() or not self.original_schema:
            raise ValueError("Expected schema to be created before setting an avatar schema")
        if tables is None:
            tables = list(self.avatar_tables.values())
        self.avatar_schema = get_schema(name, tables, schema_ref)

    def create_table(
        self,
        table_name: str,
        original_volume: str,
        original_file: str,
        avatar_volume: str | None = None,
        avatar_file: str | None = None,
        primary_key: str | None = None,
        foreign_keys: list | None = None,
        time_series_time: str | None = None,
        types: dict[str, ColumnType] | None = None,
        individual_level: bool | None = None,
    ):
        if primary_key and time_series_time and primary_key == time_series_time:
            raise ValueError(
                f"Expected primary_key and time_series_time to be different fields, got {primary_key=} and {time_series_time=}"
            )
        if primary_key and foreign_keys and (primary_key in foreign_keys):
            raise ValueError(
                f"Expected a primary_key and foreign_keys to be different fields, got {primary_key=} in {foreign_keys=}"
            )
        if time_series_time and foreign_keys and (time_series_time in foreign_keys):
            raise ValueError(
                f"Expected time_series time and foreign_keys to be different fields, got {time_series_time=} in {foreign_keys=}"
            )

        columns_infos = []
        if time_series_time:
            columns_infos.append(
                ColumnInfo(
                    field=time_series_time,
                    time_series_time=True,
                    type=types.get(time_series_time) if types else None,
                )
            )

        if primary_key:
            columns_infos.append(
                ColumnInfo(
                    field=primary_key,
                    primary_key=True,
                    type=types.get(primary_key) if types else None,
                )
            )

        if foreign_keys:
            for foreign_key in foreign_keys:
                columns_infos.append(
                    ColumnInfo(
                        field=foreign_key,
                        identifier=True,
                        type=types.get(foreign_key) if types else None,
                    )
                )
        columns_infos = columns_infos
        if types:
            for column_name, column_type in types.items():
                if column_name not in {primary_key, time_series_time, *(foreign_keys or [])}:
                    columns_infos.append(ColumnInfo(field=column_name, type=column_type))

        table_info = TableInfo(
            name=table_name,
            data=TableDataInfo(original_volume, original_file),
            columns=columns_infos if columns_infos != [] else None,
            individual_level=individual_level,
        )
        self.tables[table_name] = table_info

        if avatar_file:
            self.create_avatar_table(table_name, avatar_volume, avatar_file)

    def create_avatar_table(
        self, table_name, avatar_volume: str | None = None, avatar_file: str | None = None
    ):
        self._check_table_name(table_name)

        if avatar_file is None:
            avatars_data = TableDataInfo(auto=True)
        else:
            avatars_data = TableDataInfo(avatar_volume, avatar_file)

        table_info_avatar = TableInfo(
            name=table_name,
            avatars_data=avatars_data,
        )
        self.avatar_tables[table_name] = table_info_avatar

    def create_link(self, parent_table_name, child_table_name, parent_field, child_field, method):
        self._check_table_name(parent_table_name)
        self._check_table_name(child_table_name)

        if parent_field not in [
            column.field for column in self.tables[parent_table_name].columns if column.primary_key
        ]:
            raise ValueError(
                f"Expected field `{parent_field}` to be the primary key of the table `{parent_table_name}`"
            )
        if child_field not in [
            column.field for column in self.tables[child_table_name].columns if column.identifier
        ]:
            raise ValueError(
                f"Expected field `{child_field}` to be an identifier in table `{child_table_name}`"
            )

        parent_table = self.tables[parent_table_name]
        link_info = TableLinkInfo(
            field=parent_field,
            to=TableLinkInfoSpec(table=child_table_name, field=child_field),
            method=method,
        )

        if parent_table.links is None:
            parent_table.links = [link_info]
        else:
            parent_table.links.append(link_info)

    def create_avatarization_parameters(
        self,
        table_name: str,
        k: int,
        ncp: int | None = None,
        use_categorical_reduction: bool | None = None,
        column_weights: dict[str, float] | None = None,
        exclude_variable_names: list[str] | None = None,
        exclude_replacement_strategy: str | None = None,
        imputation_method: str | None = None,
        imputation_k: int | None = None,
        imputation_training_fraction: float | None = None,
    ):
        self._check_table_name(table_name)

        imputation = self._create_imputation_parameters(
            imputation_method, imputation_k, imputation_training_fraction
        )
        exclude_variables = self._create_exclude_variables_parameters(
            exclude_variable_names, exclude_replacement_strategy
        )

        self.avatarization[table_name] = AvatarizationParameters(
            k=k,
            ncp=ncp,
            use_categorical_reduction=use_categorical_reduction,
            column_weights=column_weights,
            exclude_variables=exclude_variables,
            imputation=imputation,
        )

    def create_time_series_parameters(
        self,
        table_name: str,
        nf: int | None = None,
        projection_type: str | None = None,
        nb_points: int | None = None,
        method: str | None = None,
    ):
        self._check_table_name(table_name)

        projection = None
        if projection_type or nf:
            self._check_parameters(projection_type, ProjectionType)
            projection = {"projection_type": projection_type, "nf": nf}

        alignment = None
        if nb_points or method:
            self._check_parameters(method, AlignmentMethod)
            alignment = {"nb_points": nb_points, "method": method}

        self.time_series[table_name] = TimeSeriesParameters(
            projection=projection, alignment=alignment
        )

    def create_signal_metrics_parameters(
        self,
        table_name: str,
        ncp: int | None = None,
        use_categorical_reduction: bool | None = None,
        imputation_method: str | None = None,
        imputation_k: int | None = None,
        imputation_training_fraction: float | None = None,
    ):
        self._check_table_name(table_name)

        imputation = self._create_imputation_parameters(
            imputation_method, imputation_k, imputation_training_fraction
        )

        if ncp or use_categorical_reduction or imputation:
            self.signal_metrics[table_name] = SignalMetricsParameters(
                ncp=ncp,
                use_categorical_reduction=use_categorical_reduction,
                imputation=imputation,
            )

    def create_privacy_metrics_parameters(
        self,
        table_name: str,
        ncp: int | None = None,
        use_categorical_reduction: bool | None = None,
        imputation_method: str | None = None,
        imputation_k: int | None = None,
        imputation_training_fraction: float | None = None,
        known_variables: list[str] | None = None,
        target: str | None = None,
        closest_rate_percentage_threshold: float | None = None,
        closest_rate_ratio_threshold: float | None = None,
        categorical_hidden_rate_variables: list[str] | None = None,
    ):
        self._check_table_name(table_name)

        imputation = self._create_imputation_parameters(
            imputation_method, imputation_k, imputation_training_fraction
        )
        if (
            ncp
            or use_categorical_reduction
            or imputation
            or known_variables
            or target
            or closest_rate_percentage_threshold
            or closest_rate_ratio_threshold
            or categorical_hidden_rate_variables
        ):
            self.privacy_metrics[table_name] = PrivacyMetricsParameters(
                ncp=ncp,
                use_categorical_reduction=use_categorical_reduction,
                known_variables=known_variables,
                target=target,
                closest_rate_percentage_threshold=closest_rate_percentage_threshold,
                closest_rate_ratio_threshold=closest_rate_ratio_threshold,
                categorical_hidden_rate_variables=categorical_hidden_rate_variables,
                imputation=imputation,
            )

    def _check_table_name(self, table_name):
        if table_name not in self.tables.keys():
            raise ValueError(
                f"Expected table `{table_name}` to be created before setting parameters"
            )

    def _check_parameters(self, parameter: str | None, object: Any):
        if parameter and parameter not in {item.value for item in object}:
            valid_values = [item.value for item in object]
            raise ValueError(
                f"Expected one of {valid_values}, got {parameter} as {object.__name__} parameter"
            )

    def _create_imputation_parameters(
        self,
        method: str | None = None,
        k: int | None = None,
        training_fraction: float | None = None,
    ):
        if method or k or training_fraction:
            self._check_parameters(method, ImputeMethod)
            return {
                "method": method,
                "k": k,
                "training_fraction": training_fraction,
            }
        return None

    def _create_exclude_variables_parameters(
        self,
        exclude_variable_names: list[str] | None = None,
        exclude_replacement_strategy: str | None = None,
    ):
        if exclude_variable_names:
            self._check_parameters(exclude_replacement_strategy, ExcludeVariablesMethod)
            return {
                "variable_names": exclude_variable_names,
                "replacement_strategy": exclude_replacement_strategy,
            }

        return None

    def create_volume(self, name, url):
        self.volume = Volume(
            kind=ModelKind.VOLUME,
            metadata=Metadata(name=name),
            spec=VolumeSpec(url=url),
        )

    def create_results_volume(self, name, url):
        self.results_volume = Volume(
            kind=ModelKind.VOLUME,
            metadata=Metadata(name=name),
            spec=VolumeSpec(url=url),
        )

    def create_report(self, report_name: str | None = None, report_type: str = "basic"):
        report_name = report_name or "report"
        if not self.results_volume:
            raise ValueError("Expected results volume to be created before setting results")
        results = Results(
            volume=self.results_volume.metadata.name,
            path="report",
        )
        self.report = ReportParameters(
            kind=ModelKind.REPORT,
            metadata=Metadata(name=report_name),
            spec=ReportParametersSpec(report_type=report_type, results=results),
        )

    def get_avatarization(self, name: str = "avatarization") -> str:
        if not self.avatarization:
            raise ValueError("No avatarization parameters have been set")
        if self.time_series == {}:
            time_series = None
        else:
            time_series = self.time_series

        if not self.results_volume:
            raise ValueError("Expected results volume to be created before setting results")
        results = Results(
            volume=self.results_volume.metadata.name,
            path="avatarization",
        )

        return get_avatarization_parameters(
            metadata=Metadata(name=name),
            schema_name=self._schema_name(),
            avatarization=self.avatarization,
            time_series=time_series,
            seed=self.seed,
            results=results,
        )

    def get_signal_metrics(
        self, name: str = "signal", avatarization_ref: str = "avatarization"
    ) -> str:
        time_series = self.time_series or None
        signal_metrics = self.signal_metrics or None

        if not self.results_volume:
            raise ValueError("Expected results volume to be created before setting results")
        results = Results(
            volume=self.results_volume.metadata.name,
            path="signal_metrics",
        )
        return get_signal_metrics_parameters(
            metadata=Metadata(name=name),
            schema_name=self._avatar_schema_name(),
            avatarization_ref=avatarization_ref,
            signal_metrics=signal_metrics,
            time_series=time_series,
            seed=self.seed,
            results=results,
        )

    def get_privacy_metrics(
        self, name: str = "privacy", avatarization_ref: str = "avatarization"
    ) -> str:
        time_series = self.time_series or None
        privacy_metrics = self.privacy_metrics or None

        if not self.results_volume:
            raise ValueError("Expected results volume to be created before setting results")
        results = Results(
            volume=self.results_volume.metadata.name,
            path="privacy_metrics",
        )
        return get_privacy_metrics_parameters(
            metadata=Metadata(name=name),
            schema_name=self._avatar_schema_name(),
            avatarization_ref=avatarization_ref,
            privacy_metrics=privacy_metrics,
            time_series=time_series,
            seed=self.seed,
            results=results,
        )

    def get_parameters(self) -> str:
        return aggregate_yamls(
            self.get_avatarization(),
            self.get_privacy_metrics(),
            self.get_signal_metrics(),
            self.get_report(),
        )

    def get_report(self) -> str:
        if self.report is None:
            self.create_report()
        return to_yaml(self.report)  # type: ignore[arg-type]

    def get_schema(self) -> str:
        if self.original_schema is None:
            self.create_schema(self._schema_name())
        return to_yaml(self.original_schema)  # type: ignore[arg-type]

    def get_avatar_schema(self) -> str:
        if self.avatar_schema is None:
            for name in self.tables.keys():
                if name not in self.avatar_tables.keys():
                    self.create_avatar_table(name)

            self.create_avatar_schema(
                self._avatar_schema_name(),
                schema_ref=self._schema_name(),
            )
        return to_yaml(self.avatar_schema)  # type: ignore[arg-type]

    def get_volume(self) -> str:
        if not self.volume:
            raise ValueError("No volume has been set")
        return to_yaml(self.volume)

    def get_result_volume(self) -> str:
        if not self.results_volume:
            raise ValueError("No results volume has been set")
        return to_yaml(self.results_volume)

    def get_yaml(self, path: str | None = None) -> str:
        yaml = aggregate_yamls(
            self.get_volume(),
            self.get_result_volume(),
            self.get_schema(),
            self.get_avatar_schema(),
            self.get_parameters(),
        )
        if path:
            with open(path, "w") as f:
                f.write(yaml)
        return yaml

    def delete_parameters(self, table_name: str, parameters_names: list[str] | None = None):
        if parameters_names:
            for parameter_name in parameters_names:
                if hasattr(self.avatarization[table_name], parameter_name):
                    setattr(self.avatarization[table_name], parameter_name, None)
                if hasattr(self.time_series, table_name) and hasattr(
                    self.time_series[table_name], parameter_name
                ):
                    setattr(self.time_series[table_name], parameter_name, None)
                if hasattr(self.privacy_metrics, table_name) and hasattr(
                    self.privacy_metrics[table_name], parameter_name
                ):
                    setattr(self.privacy_metrics[table_name], parameter_name, None)
                if hasattr(self.signal_metrics, table_name) and hasattr(
                    self.signal_metrics[table_name], parameter_name
                ):
                    setattr(self.signal_metrics[table_name], parameter_name, None)
        else:
            self.avatarization.pop(table_name, None)
            self.time_series.pop(table_name, None)
            self.privacy_metrics.pop(table_name, None)
            self.signal_metrics.pop(table_name, None)

    def delete_table(self, table_name: str):
        self.tables.pop(table_name, None)
        self.avatar_tables.pop(table_name, None)
        self.delete_parameters(table_name)

    def delete_link(self, parent_table_name, child_table_name):
        for link in self.tables[parent_table_name].links:
            if link.to.table == child_table_name:
                self.tables[parent_table_name].links.remove(link)
                break
