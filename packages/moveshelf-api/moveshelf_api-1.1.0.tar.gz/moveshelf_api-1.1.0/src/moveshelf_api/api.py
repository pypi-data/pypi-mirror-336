"""
This module provides core components for interacting with Moveshelf, including data types and an API client
for managing projects, subjects, sessions, conditions, and clips. 

Dependencies:
    - Python standard library modules: `base64`, `json`, `logging`, `re`, `struct`, `os.path`
    - Third-party modules: `requests`, `six`, `enum` (optional), `crcmod`, `mypy_extensions`
"""

import base64
import json
import logging
import re
import struct
from os import path

try:
    import enum
except ImportError:
    print('Please install enum34 package')
    raise

import requests
import six
from crcmod.predefined import mkPredefinedCrcFun
from mypy_extensions import TypedDict

logger = logging.getLogger('moveshelf-api')

class TimecodeFramerate(enum.Enum):
    """
    Enum representing supported video framerates for timecodes.

    Attributes:
        FPS_24 (str): 24 frames per second.
        FPS_25 (str): 25 frames per second.
        FPS_29_97 (str): 29.97 frames per second.
        FPS_30 (str): 30 frames per second.
        FPS_50 (str): 50 frames per second.
        FPS_59_94 (str): 59.94 frames per second.
        FPS_60 (str): 60 frames per second.
        FPS_1000 (str): 1000 frames per second.
    """
    FPS_24 = '24'
    FPS_25 = '25'
    FPS_29_97 = '29.97'
    FPS_30 = '30'
    FPS_50 = '50'
    FPS_59_94 = '59.94'
    FPS_60 = '60'
    FPS_1000 = '1000'

Timecode = TypedDict('Timecode', {
    'timecode': str,
    'framerate': TimecodeFramerate
    })
"""
A typed dictionary representing a timecode.

Keys:
    - timecode (str): The timecode string in `HH:MM:SS:FF` format.
    - framerate (TimecodeFramerate): The framerate associated with the timecode.
"""

Metadata = TypedDict('Metadata', {
    'title': str,
    'description': str,
    'previewImageUri': str,
    'allowDownload': bool,
    'allowUnlistedAccess': bool,
    'startTimecode': Timecode
    }, total=False)
"""
A typed dictionary representing metadata for a clip.

Keys:
    - title (str): The title of the clip.
    - description (str): The description of the clip.
    - previewImageUri (str): The URI for the preview image.
    - allowDownload (bool): Whether downloading is allowed.
    - allowUnlistedAccess (bool): Whether unlisted access is allowed.
    - startTimecode (Timecode): Optional start timecode for the clip.
"""

class MoveshelfApi(object):
    """
    Client for interacting with the Moveshelf API.

    This class provides methods to manage projects, subjects, sessions, conditions, and clips on the Moveshelf platform.

    Attributes:
        api_url (str): The API endpoint URL.
        _auth_token (BearerTokenAuth): Authentication token for API requests.
        _crc32c (function): CRC32C checksum function for file validation.
    """

    def __init__(self, api_key_file='mvshlf-api-key.json', api_url='https://api.moveshelf.com/graphql'):
        """
        Initialize the Moveshelf API client.

        Args:
            api_key_file (str): Path to the JSON file containing the API key. Defaults to 'mvshlf-api-key.json'.
            api_url (str): URL for the Moveshelf GraphQL API. Defaults to 'https://api.moveshelf.com/graphql'.

        Raises:
            ValueError: If the API key file is not found or invalid.
        """
        self._crc32c = mkPredefinedCrcFun('crc32c')
        self.api_url = api_url

        if not path.isfile(api_key_file):
            raise ValueError("No valid API key. Please check instructions on https://github.com/moveshelf/python-api-example")

        with open(api_key_file, 'r') as key_file:
            data = json.load(key_file)
            self._auth_token = BearerTokenAuth(data['secretKey'])

    def getProjectDatasets(self, project_id):
        """
        Retrieve datasets for a given project.

        Args:
            project_id (str): The ID of the project.

        Returns:
            list: A list of datasets, each containing `name` and `downloadUri`.
        """
        data = self._dispatch_graphql(
            '''
            query getProjectDatasets($projectId: ID!) {
            node(id: $projectId) {
                ... on Project {
                id,
                name,
                datasets {
                    name,
                    downloadUri
                }
                }
            }
            }
            ''',
            projectId=project_id
        )
        return [d for d in data['node']['datasets']]

    def getUserProjects(self):
        """
        Retrieve all projects associated with the current user.

        Returns:
            list: A list of dictionaries, each containing the `name` and `id` of a project.
        """
        data = self._dispatch_graphql(
            '''
            query {
                viewer {
                    projects {
                        name
                        id
                    }
                }
            }
            '''
        )
        return [{k: v for k, v in p.items() if k in ['name', 'id']} for p in data['viewer']['projects']]

    def createClip(self, project, metadata=Metadata()):
        """
        Create a new clip in the specified project with optional metadata.

        Args:
            project (str): The project ID.
            metadata (Metadata): Metadata for the new clip. Defaults to an empty Metadata dictionary.

        Returns:
            str: The ID of the created clip.
        """
        creation_response = self._createClip(project, {
            'clientId': 'manual',
            'metadata': metadata
        })
        logging.info('Created clip ID: %s', creation_response['mocapClip']['id'])

        return creation_response['mocapClip']['id']

    def uploadFile(self, file_path, project, metadata=Metadata()):
        """
        Upload a file to a specified project.

        Args:
            file_path (str): The local path to the file being uploaded.
            project (str): The project ID where the file will be uploaded.
            metadata (Metadata): Metadata for the file. Defaults to an empty Metadata dictionary.

        Returns:
            str: The ID of the created clip.
        """
        logger.info('Uploading %s', file_path)

        metadata['title'] = metadata.get('title', path.basename(file_path))
        metadata['allowDownload'] = metadata.get('allowDownload', False)
        metadata['allowUnlistedAccess'] = metadata.get('allowUnlistedAccess', False)

        if metadata.get('startTimecode'):
            self._validateAndUpdateTimecode(metadata['startTimecode'])

        creation_response = self._createClip(project, {
            'clientId': file_path,
            'crc32c': self._calculateCrc32c(file_path),
            'filename': path.basename(file_path),
            'metadata': metadata
        })
        logging.info('Created clip ID: %s', creation_response['mocapClip']['id'])

        with open(file_path, 'rb') as fp:
            requests.put(creation_response['uploadUrl'], data=fp)

        return creation_response['mocapClip']['id']

    def uploadAdditionalData(self, file_path, clipId, dataType, filename):
        """
        Upload additional data to an existing clip.

        Args:
            file_path (str): The local path to the file being uploaded.
            clipId (str): The ID of the clip to associate with the data.
            dataType (str): The type of the additional data (e.g., 'video', 'annotation').
            filename (str): The name to assign to the uploaded file.

        Returns:
            str: The ID of the uploaded data.
        """
        logger.info('Uploading %s', file_path)

        creation_response = self._createAdditionalData(clipId, {
            'clientId': file_path,
            'crc32c': self._calculateCrc32c(file_path),
            'filename': filename,
            'dataType': dataType
        })
        logging.info('Created clip ID: %s', creation_response['data']['id'])

        with open(file_path, 'rb') as fp:
            requests.put(creation_response['uploadUrl'], data=fp)

        return creation_response['data']['id']

    def updateClipMetadata(self, clip_id, metadata):
        """
        Update the metadata for an existing clip.

        Args:
            clip_id (str): The ID of the clip to update.
            metadata (Metadata): The updated metadata for the clip.

        Returns:
            None
        """
        logger.info('Updating metadata for clip: %s', clip_id)

        if metadata.get('startTimecode'):
            self._validateAndUpdateTimecode(metadata['startTimecode'])

        res = self._dispatch_graphql(
            '''
            mutation updateClip($input: UpdateClipInput!) {
                updateClip(clipData: $input) {
                    clip {
                        id
                    }
                }
            }
            ''',
            input={
                'id': clip_id,
                'metadata': metadata
            }
        )
        logging.info('Updated clip ID: %s', res['updateClip']['clip']['id'])

    def createSubject(self, project_id, name):
        """
        Create a new subject within a project.

        Args:
            project_id (str): The ID of the project where the subject will be created.
            name (str): The name of the new subject.

        Returns:
            dict: A dictionary containing the `id` and `name` of the created subject.
        """
        data = self._dispatch_graphql(
            '''
                mutation createPatientMutation($projectId: String!, $name: String!) {
                    createPatient(projectId: $projectId, name: $name) {
                        patient {
                            id
                            name
                        }
                    }
                }
            ''',
            projectId=project_id,
            name=name
        )

        return data['createPatient']['patient']

    def updateSubjectMetadataInfo(self, subject_id, info_to_save):
        """
        Update the metadata for an existing subject.

        Args:
            subject_id (str): The ID of the subject to update.
            info_to_save (dict): The metadata to save for the subject.

        Returns:
            bool: Whether the metadata update was successful.
        """
        data = self._dispatch_graphql(
            '''
                mutation updatePatientMutation($patientId: ID!, $metadata: JSONString) {
                    updatePatient(patientId: $patientId, metadata: $metadata) {
                        updated
                    }
                }
            ''',
            patientId=subject_id,
            metadata=info_to_save
        )

        return data['updatePatient']['updated']

    def getSubjectContext(self, subject_id):
        """
        Retrieve the context information for a specific subject.

        Args:
            subject_id (str): The ID of the subject to retrieve.

        Returns:
            dict: A dictionary containing subject details such as ID, name, metadata, 
                  and associated project information (i.e., project ID, description, canEdit permission, and unlistedAccess permission).
        """
        data = self._dispatch_graphql(
            '''
                query getPatientContext($patientId: ID!) {
                    node(id: $patientId) {
                        ... on Patient {
                            id,
                            name,
                            metadata,
                            project {
                                id
                                description
                                canEdit
                                unlistedAccess
                            }
                        }
                    }
                }
            ''',
            patientId=subject_id
        )

        return data['node']

    def createSession(self, project_id, session_path, subject_id):
        """
        Create a session for a specified subject within a project.

        Args:
            project_id (str): The ID of the project where the session will be created.
            session_path (str): The path to associate with the session.
            subject_id (str): The ID of the subject for whom the session is created.

        Returns:
            dict: A dictionary containing the session's ID and project path.
        """
        data = self._dispatch_graphql(
            '''
                mutation createSessionMutation($projectId: String!, $projectPath: String!, $patientId: ID!) {
                    createSession(projectId: $projectId, projectPath: $projectPath, patientId: $patientId) {
                        session {
                            id
                            projectPath
                        }
                    }
                }
            ''',
            projectId=project_id,
            projectPath=session_path,
            patientId=subject_id
        )

        return data['createSession']['session']
    
    def updateSessionMetadataInfo(self, session_id, session_name, session_metadata, session_date = None, previous_updated_at = None):
        """
        Update the metadata for an existing session.

        Args:
            session_id (str): The ID of the session to update.
            session_name (str): The new name for the session to update.
            session_metadata (dict): The metadata to save for the session.
            session_date (str): The new date for the session to update. If empty, skips update of session date. Defaults to None.
            previous_updated_at (str): The previous updated in ISO format. If empty, force update. Defaults to None.

        Returns:
            bool: Whether the metadata update was successful.
        """
        data = self._dispatch_graphql(
            '''
                mutation updateSession($sessionId: ID!, $sessionName: String!, $sessionMetadata: JSONString, $sessionDate: String, $previousUpdatedAt: String) {
                    updateSession(
                        sessionId: $sessionId,
                        sessionName: $sessionName,
                        sessionMetadata: $sessionMetadata,
                        sessionDate: $sessionDate,
                        previousUpdatedAt: $previousUpdatedAt
                    ) {
                        updated
                    }
                }
            ''',
            sessionId=session_id,
            sessionName=session_name,
            sessionMetadata=session_metadata,
            sessionDate=session_date,
            previousUpdatedAt=previous_updated_at
        )

        return data['updateSession']['updated']

    def getProjectClips(self, project_id, limit, include_download_link=False):
        """
        Retrieve clips from a specified project.

        Args:
            project_id (str): The ID of the project from which to fetch clips.
            limit (int): The maximum number of clips to retrieve.
            include_download_link (bool): Whether to include download link information in the result. Defaults to False.

        Returns:
            list: A list of dictionaries, each containing clip information such as ID, title, and project path. 
                  If `include_download_link` is True, includes file name and download URI.
        """
        query = '''
            query getAdditionalDataInfo($projectId: ID!, $limit: Int) {
            node(id: $projectId) {
                ... on Project {
                id,
                name,
                clips(first: $limit) {
                edges {
                    node {
                        id,
                        title,
                        projectPath
                    }
                    }
                }
                }
            }
            }
            '''
        if include_download_link:
            query = '''
                query getAdditionalDataInfo($projectId: ID!, $limit: Int) {
                node(id: $projectId) {
                    ... on Project {
                    id,
                    name,
                    clips(first: $limit) {
                    edges {
                        node {
                            id,
                            title,
                            projectPath
                            originalFileName
                            originalDataDownloadUri
                        }
                        }
                    }
                    }
                }
                }
                '''

        data = self._dispatch_graphql(
            query,
            projectId=project_id,
            limit=limit
        )

        return [c['node'] for c in data['node']['clips']['edges']]

    def getAdditionalData(self, clip_id):
        """
        Retrieve additional data associated with a specific clip.

        Args:
            clip_id (str): The ID of the clip for which to fetch additional data.

        Returns:
            list: A list of dictionaries, each containing details about additional data, including:
                  ID, data type, upload status, original file name, preview data URI, 
                  and original data download URI.
        """
        data = self._dispatch_graphql(
            '''
            query getAdditionalDataInfo($clipId: ID!) {
            node(id: $clipId) {
                ... on MocapClip {
                id,
                additionalData {
                    id
                    dataType
                    uploadStatus
                    originalFileName
                    previewDataUri
                    originalDataDownloadUri
                }
                }
            }
            }
            ''',
            clipId=clip_id
        )

        return data['node']['additionalData']

    def getClipData(self, clip_id):
        """
        Retrieve information about a specific clip.

        Args:
            clip_id (str): The ID of the clip to retrieve.

        Returns:
            dict: A dictionary containing the clip's ID, title, and description.
        """
        data = self._dispatch_graphql(
            '''
            query getClipInfo($clipId: ID!) {
            node(id: $clipId) {
                ... on MocapClip {
                id,
                title,
                description
                }
            }
            }
            ''',
            clipId=clip_id
        )

        return data['node']

    def getProjectAndClips(self):
        """
        Retrieve a list of all projects and the first 20 clips associated with each project.

        Returns:
            list: A list of dictionaries, where each dictionary contains project details 
                  (ID and name) and a nested list of clip details (ID and title).
        """
        data = self._dispatch_graphql(
            '''
            query {
                viewer {
                    projects {
                        id
                        name
                        clips(first: 20) {
                            edges {
                                node {
                                    id,
                                    title
                                    }
                                }
                            }
                    }
                }
            }
            '''
        )
        return [p for p in data['viewer']['projects']]
    
    def getProjectSubjects(self, project_id):
        """
        Retrieve all subjects (patients) associated with a specific project.

        Args:
            project_id (str): The ID of the project to retrieve subjects for.

        Returns:
            list: A list of dictionaries, each containing the subject's ID, name, update date, and externalId (i.e., EHR-ID/MRN).
        """
        data = self._dispatch_graphql(
            '''
            query getProjectPatients($projectId: ID!) {
                node(id: $projectId) {
                    ... on Project {
                        id,
                        name,
                        description,
                        configuration,
                        canEdit,
                        template {
                            name,
                            data  
                        },
                        patientsList {
                            id
                            name
                            updated
                            externalId
                        }
                    }
                }
            }
            ''',
            projectId=project_id
        )
        return data['node']['patientsList']
    
    def getProjectSubjectByEhrId(self, ehr_id, project_id):
        """
        Retrieve the subject with the specified ehr_id associated with a specific project.

        Args:
            ehr_id (str): The EHR-ID/MRN of the subject to be retrieved
            project_id (str): The ID of the project to retrieve the subject for.
        Returns:
            dict: A dictionary containing the subject's ID and name. Returns None if no subject with
                matching EHR-ID/MRN exists in the specified project.
        """
        data = self._dispatch_graphql(
            '''
            query getPatientByEhrId($ehrId: String!, $projectId: String!) {
                patient(ehrId: $ehrId, projectId: $projectId) {
                id
                name
                }
            }
            ''',
            ehrId=ehr_id,
            projectId=project_id
        )
        return data['patient']

    def getSubjectDetails(self, subject_id):
        """
        Retrieve details about a specific subject, including metadata, 
        associated projects, reports, sessions, clips, and norms.

        Args:
            subject_id (str): The ID of the subject to retrieve.

        Returns:
            dict: A dictionary containing the subject's details, including:
                  - ID, name, and metadata.
                  - Associated project details (ID).
                  - List of reports (ID and title).
                  - List of sessions with nested clips and norms details.
        """
        data = self._dispatch_graphql(
            '''
            query getPatient($patientId: ID!) {
                node(id: $patientId) {
                    ... on Patient {
                        id,
                        name,
                        metadata,
                        project {
                            id
                        }
                        reports {
                            id
                            title
                        }
                        sessions {
                            id
                            projectPath
                            clips {
                                id
                                title
                                created
                                projectPath
                                uploadStatus
                                hasCharts
                            }
                            norms {
                                id
                                name
                                uploadStatus
                                projectPath
                                clips {
                                    id
                                    title
                                }
                            }
                        }
                    }
                }
            }
            ''',
            patientId=subject_id
        )
        return data['node']

    def processGaitTool(self, clip_ids, trial_type):
        """
        Submit a Gait Tool processing job for the specified clips and trial type.

        Args:
            clip_ids (list): A list of clip IDs to process.
            trial_type (str): The trial type for the processing job.

        Returns:
            str: The job ID of the created processing task.
        """
        data = self._dispatch_graphql(
            '''
            mutation processGaitTool($clips: [String!], $trialType: String) {
                processGaitTool(clips: $clips, trialType: $trialType) {
                    jobId
                }
            }
            ''',
            clips=clip_ids,
            trialType=trial_type
        )
        return data['processGaitTool']['jobId']

    def getJobStatus(self, job_id):
        """
        Retrieve the status of a specific job by its ID.

        Args:
            job_id (str): The ID of the job to check.

        Returns:
            dict: A dictionary containing the job's ID, status, result, and description.
        """
        data = self._dispatch_graphql(
            '''
            query jobStatus($jobId: ID!) {
                node(id: $jobId) {
                    ... on Job {
                        id,
                        status,
                        result,
                        description
                    }
                }
            }
            ''',
            jobId=job_id
        )
        return data['node']

    def getSessionById(self, session_id):
        """
        Retrieve detailed information about a session by its ID.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            dict: A dictionary containing session details, including:
                  - ID, projectPath, and metadata.
                  - Associated project, clips, norms, and patient information.
        """
        data = self._dispatch_graphql(
            '''
            query getSession($sessionId: ID!) {
                node(id: $sessionId) {
                    ... on Session {
                        id,
                        projectPath,
                        metadata,
                        project {
                            id
                            name
                            canEdit
                        }
                        clips {
                            id
                            title
                            created
                            projectPath
                            uploadStatus
                            hasCharts
                            hasVideo
                        }
                        norms {
                            id
                            name
                            uploadStatus
                            projectPath
                            clips {
                                id
                                title
                            }
                        }
                        patient {
                        id
                        name
                        }
                    }
                }
            }
            ''',
            sessionId=session_id
        )
        return data['node']

    def _validateAndUpdateTimecode(self, tc):
        """
        Validate and update a timecode dictionary.

        Args:
            tc (dict): A dictionary containing timecode and framerate information.

        Raises:
            AssertionError: If timecode or framerate is invalid.
        """
        assert tc.get('timecode')
        assert tc.get('framerate')
        assert isinstance(tc['framerate'], TimecodeFramerate)
        assert re.match('\d{2}:\d{2}:\d{2}[:;]\d{2,3}', tc['timecode'])
        tc['framerate'] = tc['framerate'].name

    def _createClip(self, project, clip_creation_data):
        """
        Create a new clip in the specified project.

        Args:
            project (str): The ID of the project where the clip will be created.
            clip_creation_data (dict): The data required to create the clip.

        Returns:
            dict: A dictionary containing the client ID, upload URL, and clip ID.
        """
        data = self._dispatch_graphql(
            '''
            mutation createClip($input: ClipCreationInput!) {
                createClips(input: $input) {
                    response {
                        clientId,
                        uploadUrl,
                        mocapClip {
                            id
                        }
                    }
                }
            }
            ''',
            input={
                'project': project,
                'clips': [clip_creation_data]
            }
        )
        return data['createClips']['response'][0]

    def _calculateCrc32c(self, file_path):
        """
        Calculate the CRC32C checksum of a file.

        Args:
            file_path (str): The path to the file to calculate the checksum for.

        Returns:
            str: The Base64-encoded CRC32C checksum.
        """
        with open(file_path, 'rb') as fp:
            crc = self._crc32c(fp.read())
            b64_crc = base64.b64encode(struct.pack('>I', crc))
            return b64_crc if six.PY2 else b64_crc.decode('utf8')

    def _createAdditionalData(self, clipId, metadata):
        """
        Create additional data for a specific clip.

        Args:
            clipId (str): The ID of the clip to associate the additional data with.
            metadata (dict): Metadata for the additional data, including data type and filename.

        Returns:
            dict: A dictionary containing the upload URL and data details (ID, type, and upload status).
        """
        data = self._dispatch_graphql(
            '''
            mutation createAdditionalData($input: CreateAdditionalDataInput) {
                createAdditionalData(input: $input) {
                uploadUrl
                data {
                    id
                    dataType
                    originalFileName
                    uploadStatus
                }
                }
            }
            ''',
            input={
                'clipId': clipId,
                'dataType': metadata['dataType'],
                'crc32c': metadata['crc32c'],
                'filename': metadata['filename'],
                'clientId': metadata['clientId']
            }
        )
        return data['createAdditionalData']

    def _dispatch_graphql(self, query, **kwargs):
        """
        Send a GraphQL query or mutation to the API and return the response data.

        Args:
            query (str): The GraphQL query or mutation string.
            **kwargs: Variables to be passed into the GraphQL query.

        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
            GraphQlException: If the GraphQL response contains errors.

        Returns:
            dict: The `data` field from the GraphQL response, containing the requested information.
        """
        payload = {
            'query': query,
            'variables': kwargs
        }
        response = requests.post(self.api_url, json=payload, auth=self._auth_token)
        response.raise_for_status()

        json_data = response.json()
        if 'errors' in json_data:
            raise GraphQlException(json_data['errors'])

        return json_data['data']


class BearerTokenAuth(requests.auth.AuthBase):
    """
    A custom authentication class for using Bearer tokens with HTTP requests.

    Attributes:
        _auth (str): The formatted Bearer token string.
    """

    def __init__(self, token):
        """
        Initialize the BearerTokenAuth instance with a token.

        Args:
            token (str): The Bearer token to use for authentication.
        """
        self._auth = 'Bearer {}'.format(token)

    def __call__(self, request):
        """
        Modify the request to include the Bearer token in the Authorization header.

        Args:
            request (requests.PreparedRequest): The HTTP request object.

        Returns:
            requests.PreparedRequest: The modified HTTP request object.
        """
        request.headers['Authorization'] = self._auth
        return request


class GraphQlException(Exception):
    """
    An exception raised when a GraphQL response contains errors.

    Attributes:
        error_info (list): A list of error information returned by the GraphQL API.
    """

    def __init__(self, error_info):
        """
        Initialize the GraphQlException with error information.

        Args:
            error_info (list): The list of errors from the GraphQL response.
        """
        self.error_info = error_info
