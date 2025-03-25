from arcanna_mcp_input_server.environment import ARCANNA_HOST

# event ingestion
SEND_EVENT_URL = ARCANNA_HOST + "/api/v1/events"
SEND_EVENT_WITH_ID_URL = ARCANNA_HOST + "/api/v1/events/{}"

# event retrieval
RETRIEVE_EVENT_BY_ID_URL = ARCANNA_HOST + "/api/v1/events/{}/{}"  # /job_id/event_id

# event feedback
EVENT_FEEDBACK_URL = ARCANNA_HOST + "/api/v1/events/{}/{}/feedback"

GET_JOBS_URL = ARCANNA_HOST + "/api/v1/jobs"
GET_JOB_BY_ID_URL = ARCANNA_HOST + "/api/v1/jobs/{}"
GET_JOB_LABELS_URL = ARCANNA_HOST + "/api/v1/jobs/{}/labels"
GET_JOB_BY_NAME_URL = ARCANNA_HOST + "/api/v1/jobs/get_by_name"
GET_JOB_LABELS_URL = ARCANNA_HOST + "/api/v1/jobs/{}/labels"
# healthcheck
HEALTH_CHECK_URL = ARCANNA_HOST + "/api/v1/health/"

