"""
Util functions for the app.
"""

import os
import datetime
import shutil
from copy import deepcopy
from pandas import DataFrame
from babylab.src import api


def format_ppt_id(ppt_id: str) -> str:
    """Format appointment ID.

    Args:
        ppt_id (str): Participant ID.

    Returns:
        str: Formated participant ID.
    """
    return f"<a href=/participants/{ppt_id}>{ppt_id}</a>"


def format_apt_id(apt_id: str) -> str:
    """Format appointment ID.

    Args:
        apt_id (str): Appointment ID.

    Returns:
        str: Formated appointment ID.
    """
    return f"<a href=/appointments/{apt_id}>{apt_id}</a>"


def format_que_id(que_id: str) -> str:
    """Format questionnaire ID.

    Args:
        apt_id (str): Questionnaire ID.
        ppt_id (str): Participant ID.

    Returns:
        str: Formated questionnaire ID.
    """
    return f"<a href=/questionnaires/{que_id}>{que_id}</a>"


def format_isestimated(isestimated: str) -> str:
    """Format ``isestimated`` variable.

    Args:
        isestimated (str): Value of ``isestimated`` variable.

    Returns:
        str: Formatted ``isestimated`` value.
    """
    return "Estimated" if isestimated == "1" else "Calculated"


def format_percentage(x: float | int) -> str:
    """Format number into percentage.

    Args:
        x (float | int): Number to format. Must be higher than or equal to zero, and lower than or equal to one.

    Raises:
        ValueError: If number is not higher than or equal to zero, and lower than or equal to one.

    Returns:
        str: Formatted percentage.
    """  # pylint: disable=line-too-long
    if x > 100 or x < 0:
        raise ValueError(
            "`x` higher than or equal to zero, and lower than or equal to one"
        )
    return str(int(float(x))) if x else ""


def format_taxi_isbooked(address: str, isbooked: str) -> str:
    """Format ``taxi_isbooked`` variable to HTML.

    Args:
        address (str): ``taxi_address`` value.
        isbooked (str): ``taxi_isbooked`` value.

    Raises:
        ValueError: If ``isbooked`` is not "0" or "1".

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if str(isbooked) not in ["", "0", "1"]:
        raise ValueError(
            f"`is_booked` must be one of '0' or '1', but {isbooked} was provided"
        )
    if not address:
        return ""
    if int(isbooked):
        return "<p style='color: green;'>Yes</p>"
    return "<p style='color: red;'>No</p>"


def format_new_button(record: str, ppt_id: str = None):
    """Add new record button.

    Args:
        record (str): Type of record.
        ppt_id (str): Participant ID.

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if record not in ["Appointment", "Questionnaire"]:
        raise ValueError(
            f"`record` must be 'Appointment' or 'Questionnaire', but {record} was provided"
        )
    status = "success" if record == "Appointment" else "primary"
    button_str = f'<button type="button" class="btn btn-{status}"><i class="fa-solid fa-plus"></i>&nbsp;&nbsp;{record}</button></a>'
    if record == "Appointment":
        return f'<a href="/appointments/appointment_new?ppt_id={ppt_id}">{button_str}'

    return f'<a href="/questionnaires/questionnaire_new?ppt_id={ppt_id}">{button_str}'


def format_modify_button(ppt_id: str = None, apt_id: str = None, que_id: str = None):
    """Add modify button.

    Args:
        ppt_id (str): Participant ID.
        apt_id (str, optional): Appointment ID. Defaults to None.
        que_id (str, optional): Questionnaire ID. Defaults to None.

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    button_str = '<button type="button" class="btn btn-warning"><i class="fa-solid fa-pen"></i>&nbsp;&nbsp;Modify</button></a>'

    if apt_id:
        return f'<a href="/appointments/{apt_id}/appointment_modify">{button_str}'

    if que_id:
        return f'<a href="/questionnaires/{que_id}/questionnaire_modify">{button_str}'

    return f'<a href="/participants/{ppt_id}/participant_modify">{button_str}'


def format_df(
    x: DataFrame,
    data_dict: dict,
    prefixes: list[str] = None,
) -> DataFrame:
    """Reformat dataframe.

    Args:
        x (DataFrame): Dataframe to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``api.get_data_dict``.
        prefixes (list[str]): List of prefixes to look for in variable names.

    Returns:
        DataFrame: A reformated Dataframe.
    """
    if prefixes is None:
        prefixes = ["participant", "appointment", "language"]
    for col_name, col_values in x.items():
        kdict = [x + "_" + col_name for x in prefixes]
        for k in kdict:
            if k in data_dict:
                x[col_name] = [data_dict[k][v] if v else "" for v in col_values]
        if "lang" in col_name:
            x[col_name] = ["" if v == "None" else v for v in x[col_name]]
        if "exp" in col_name:
            x[col_name] = [format_percentage(v) for v in col_values]
        if "taxi_isbooked" in col_name:
            pairs = zip(x["taxi_address"], x[col_name])
            x[col_name] = [format_taxi_isbooked(a, i) for a, i in pairs]
        if "isestimated" in col_name:
            x[col_name] = [format_isestimated(x) for x in x[col_name]]
    return x


def format_dict(x: dict, data_dict: dict) -> dict:
    """Reformat dictionary.

    Args:
        x (dict): dictionary to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``api.get_data_dict``.

    Returns:
        dict: A reformatted dictionary.
    """
    fields = ["participant_", "appointment_", "language_"]
    y = dict(x)
    for k, v in y.items():
        for f in fields:
            kdict = f + k
            if kdict in data_dict and v:
                y[k] = data_dict[kdict][v]
        if "exp" in k:
            y[k] = round(float(v), None) if v else ""
        if "taxi_isbooked" in k:
            y[k] = format_taxi_isbooked(y["taxi_address"], y[k])

    return y


def replace_labels(x: DataFrame | dict, data_dict: dict) -> DataFrame:
    """Replace field values with labels.

    Args:
        x (DataFrame): Pandas DataFrame in which to replace values with labels.
        data_dict (dict): Data dictionary as returned by ``get_data_dictionary``.

    Returns:
        DataFrame: A Pandas DataFrame with replaced labels.
    """  # pylint: disable=line-too-long
    if isinstance(x, DataFrame):
        return format_df(x, data_dict)
    if isinstance(x, dict):
        return format_dict(x, data_dict)
    return None


def get_age_timestamp(
    apt_records: dict, ppt_records: dict, timestamp: str = "date"
) -> tuple[str, str]:
    """Get age at timestamp in months and days.

    Args:
        apt_records (dict): Appointment records.
        ppt_records (dict): Participant records.
        timestamp (str, optional): Timestamp at which to calculate age. Defaults to "date".

    Raises:
        ValueError: If tiemstamp is not "date" or "date_created".

    Returns:
        tuple[str, str]: Age at timestamp in months and days.
    """
    if timestamp not in ["date", "date_created"]:
        raise ValueError("timestamp must be 'date' or 'date_created'")
    date_format = "%Y-%m-%d %H:%M" if timestamp == "date" else "%Y-%m-%d %H:%M:%S"
    months_new = []
    days_new = []
    for v in apt_records.values():
        if timestamp == "date_created":
            t = datetime.datetime.strptime(
                ppt_records[v.record_id].data[timestamp],
                date_format,
            )
        else:
            t = datetime.datetime.strptime(
                v.data["date"],
                "%Y-%m-%d %H:%M",
            )
        months = ppt_records[v.record_id].data["age_now_months"]
        days = ppt_records[v.record_id].data["age_now_days"]
        age_now = api.get_age(
            birth_date=api.get_birth_date(age=(months, days)),
            timestamp=t,
        )
        months_new.append(int(age_now[0]))
        days_new.append(int(age_now[1]))
    return months_new, days_new


def get_participants_table(records: api.Records, data_dict: dict) -> DataFrame:
    """Get participants table

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict, optional): Data dictionary as returned by ``api.get_data_dictionary``.

    Returns:
        DataFrame: Table of partcicipants.
    """  # pylint: disable=line-too-long
    cols = [
        "record_id",
        "date_created",
        "date_updated",
        "source",
        "name",
        "age_created_months",
        "age_created_days",
        "days_since_last_appointment",
        "sex",
        "twin",
        "parent1_name",
        "parent1_surname",
        "email1",
        "phone1",
        "parent2_name",
        "parent2_surname",
        "email2",
        "phone2",
        "address",
        "city",
        "postcode",
        "birth_type",
        "gest_weeks",
        "birth_weight",
        "head_circumference",
        "apgar1",
        "apgar2",
        "apgar3",
        "hearing",
        "diagnoses",
        "comments",
    ]
    if not records.participants.records:
        return DataFrame([], columns=cols)

    new_age_months = []
    new_age_days = []
    for _, v in records.participants.records.items():
        timestamp = datetime.datetime.strptime(
            v.data["date_created"], "%Y-%m-%d %H:%M:%S"
        )
        age_created = (v.data["age_created_months"], v.data["age_created_days"])
        birth_date = api.get_birth_date(age=age_created, timestamp=timestamp)
        age = api.get_age(birth_date=birth_date)
        new_age_months.append(int(age[0]))
        new_age_days.append(int(age[1]))

    df = records.participants.to_df()
    df["age_now_months"] = new_age_months
    df["age_now_days"] = new_age_days
    return replace_labels(df, data_dict)


def get_appointments_table(
    records: api.Records,
    data_dict: dict = None,
    study: str = None,
) -> DataFrame:
    """Get appointments table.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (str, optional): Study to filter for. Defaults to None.

    Returns:
        DataFrame: Table of appointments.
    """  # pylint: disable=line-too-long
    apts = deepcopy(records.appointments)

    if study:
        apts.records = {
            k: v for k, v in apts.records.items() if v.data["study"] == study
        }

    if not apts.records:
        return DataFrame(
            [],
            columns=[
                "appointment_id",
                "record_id",
                "study",
                "status",
                "date",
                "date_created",
                "date_updated",
                "taxi_address",
                "taxi_isbooked",
            ],
        )
    apt_records = apts.records
    if isinstance(records, api.Records):
        ppt_records = records.participants.records
    else:
        ppt_records = {records.record_id: api.RecordList(records).records}

    df = apts.to_df()
    df["appointment_id"] = [
        api.make_id(i, apt_id)
        for i, apt_id in zip(df.index, df["redcap_repeat_instance"])
    ]

    # get current age
    age_now = get_age_timestamp(apt_records, ppt_records, "date_created")
    df["age_now_months"] = age_now[0]
    df["age_now_days"] = age_now[1]

    # get age at appointment
    age_apt = get_age_timestamp(apt_records, ppt_records, "date")
    df["age_apt_months"] = age_apt[0]
    df["age_apt_days"] = age_apt[1]

    return replace_labels(df, data_dict)


def get_questionnaires_table(records: api.Records, data_dict: dict) -> DataFrame:
    """Get questionnaires table.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (str, optional): Study to filter for. Defaults to None.

    Returns:
        DataFrame: A formated Pandas DataFrame.
    """  # pylint: disable=line-too-long
    quest = records.questionnaires

    if not quest.records:
        return DataFrame(
            [],
            columns=[
                "record_id",
                "questionnaire_id",
                "isestimated",
                "date_created",
                "date_updated",
                "lang1",
                "lang1_exp",
                "lang2",
                "lang2_exp",
                "lang3",
                "lang3_exp",
                "lang4",
                "lang4_exp",
            ],
        )
    df = quest.to_df()
    df["questionnaire_id"] = [
        api.make_id(p, q) for p, q in zip(df.index, df["redcap_repeat_instance"])
    ]
    return replace_labels(df, data_dict)


def count_col(
    x: DataFrame,
    col: str,
    values_sort: bool = False,
    cumulative: bool = False,
    missing_label: str = "Missing",
) -> dict:
    """Count frequencies of column in DataFrame.

    Args:
        x (DataFrame): DataFrame containing the target column.
        col (str): Name of the column.
        values_sort (str, optional): Should the resulting dict be ordered by values? Defaults to False.
        cumulative (bool, optional): Should the counts be cumulative? Defaults to False.
        missing_label (str, optional): Label to associate with missing values. Defaults to "Missing".

    Returns:
        dict: Counts of each category, sorted in descending order.
    """  # pylint: disable=line-too-long
    counts = x[col].value_counts().to_dict()
    counts = {missing_label if not k else k: v for k, v in counts.items()}
    counts = dict(sorted(counts.items()))
    if values_sort:
        counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    if cumulative:
        for idx, (k, v) in enumerate(counts.items()):
            if idx > 0:
                counts[k] = v + list(counts.values())[idx - 1]
    return counts


def clean_tmp(path: str = "tmp"):
    """Clean temporal directory

    Args:
        path (str, optional): Path to the temporal directory. Defaults to "tmp".
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def prepare_email(ppt_id: str, apt_id: str, data: dict, data_dict: dict) -> dict:
    """Prepare email to send.

    Args:
        ppt_id (str): Participant ID.
        apt_id (str): Appointment ID.
        data (dict): Appointment data.

    Returns:
        dict: Email data.
    """
    timestamp = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M").isoformat()
    email = {
        "record_id": ppt_id,
        "id": apt_id,
        "status": data["status"],
        "date": timestamp,
        "study": data["study"],
        "taxi_address": data["taxi_address"],
        "taxi_isbooked": data["taxi_isbooked"],
        "comments": data["comments"],
    }
    return replace_labels(email, data_dict)
