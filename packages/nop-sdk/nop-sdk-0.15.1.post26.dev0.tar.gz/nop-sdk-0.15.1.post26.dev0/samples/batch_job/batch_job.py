import os
import turing
import turing.batch
import turing.batch.config
import turing.batch.config.source
from samples.common import MyEnsembler

SERVICE_ACCOUNT_NAME = "service-account@gcp-project.iam.gserviceaccount.com"

def main(turing_api: str, project: str):
    turing.set_url(turing_api)
    turing.set_project(project)
    
    ensembler = turing.PyFuncEnsembler.create(
        name="batch-ensembler-4",
        ensembler_instance=MyEnsembler(),
        conda_env={
            "dependencies": [
                "python>=3.10.0",
            ]
        },
        code_dir=[os.path.join(os.path.dirname(__file__), "../../samples")],
    )
    test_env = "dev"
    test_id = "00001"
    source = turing.batch.config.source.BigQueryDataset(
        query=f"""
            WITH customer_filter AS (
              SELECT customer_id, treatment
              FROM `gods-{test_env}.playground.turing_batch_e2e_target_list_{test_id}`
              WHERE target_date = DATE("2021-03-15", "Asia/Jakarta")
            ),
            serving_features AS (
              SELECT *
              FROM `gods-{test_env}.playground.turing_batch_e2e_features_{test_id}`
            )
            SELECT
              serving_features.*,
              customer_filter.treatment
            FROM
              customer_filter
              LEFT JOIN serving_features USING (customer_id)
        """,
        options={"viewsEnabled": "true", "materializationDataset": "playground"},
    ).join_on(columns=["customer_id", "target_date"])
    # Configure dataset(s), that contain predictions of individual models:
    predictions = {
        "model_odd": turing.batch.config.source.BigQueryDataset(
            table=f"gods-{test_env}.playground.turing_batch_e2e_predictions_model_b_{test_id}",
            features=["customer_id", "target_date", "predictions"],
        )
        .join_on(columns=["customer_id", "target_date"])
        .select(columns=["predictions"]),
        "model_even": turing.batch.config.source.BigQueryDataset(
            table=f"gods-{test_env}.playground.turing_batch_e2e_predictions_model_a_{test_id}",
            features=["customer_id", "target_date", "predictions"],
        )
        .join_on(columns=["customer_id", "target_date"])
        .select(columns=["predictions"]),
    }
    # Configure ensembling result:
    result_config = turing.batch.config.ResultConfig(
        type=turing.batch.config.ResultType.DOUBLE,
        column_name="results",
    )
    # Determine the correct staging_bucket prefix to use
    match test_env:
        case "dev":
            staging_bucket_prefix = "d"
        case "staging":
            staging_bucket_prefix = "s"
        case "production":
            staging_bucket_prefix = "p"
        case other:
            staging_bucket_prefix = ""
    # Configure destination, where ensembling results will be stored:
    sink = (
        turing.batch.config.sink.BigQuerySink(
            table=f"gods-{test_env}.playground.turing_batch_e2e_ensembling_results_{test_id}",
            staging_bucket=f"{staging_bucket_prefix}-gods-mlp",
            options={"partition_field": "target_date"},
        )
        .save_mode(turing.batch.config.sink.SaveMode.OVERWRITE)
        .select(columns=["customer_id as customerId", "target_date", "results"])
    )
    env_vars = {
        "SOME_TEST_VAR": "very_variable",
    }
    # Submit the job for execution:
    job = ensembler.submit_job(
        turing.batch.config.EnsemblingJobConfig(
            source=source,
            predictions=predictions,
            result_config=result_config,
            sink=sink,
            service_account="ci_e2e_test_secret",
            env_vars=env_vars,
            secrets=[
                turing.mounted_mlp_secret.MountedMLPSecret(
                    mlp_secret_name="ci_e2e_test_secret", env_var_name="ENV_CI_E2"
                )
            ],
        )
    )

if __name__ == "__main__":
    import fire

    fire.Fire(main)
