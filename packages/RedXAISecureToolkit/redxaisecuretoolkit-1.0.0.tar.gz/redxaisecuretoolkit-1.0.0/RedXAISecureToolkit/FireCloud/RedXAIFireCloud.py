import firebase_admin
from firebase_admin import credentials, db, firestore
from dotenv import load_dotenv
import os
from google.cloud import storage
import json



def RedXAIFirebaseInitialize(
    env_path=None,
    credentials_path=None,
    database_url=None,
    credentials_env="FIREBASE_CREDENTIALS",
    url_env="FIREBASE_DATABASE_URL"
):
    """
    Initialize Firebase Realtime Database.

    Usage Options:
    1. Pass `credentials_path` and `database_url` directly.
    2. Pass `env_path` only — uses default env variables.
    3. Pass `env_path` + `credentials_env` + `url_env` to override variable names.

    Args:
        env_path (str, optional): Path to .env file. If set, loads env variables.
        credentials_path (str, optional): Direct path to Firebase service account JSON.
        database_url (str, optional): Firebase Realtime Database URL.
        credentials_env (str): Name of the env variable for credentials (default: FIREBASE_CREDENTIALS)
        url_env (str): Name of the env variable for DB URL (default: FIREBASE_DATABASE_URL)

    Returns:
        (db, app) tuple, or (None, None) on failure.
    """
    try:
        if env_path:
            load_dotenv(env_path)
            print(f"🔍 Loaded .env from: {env_path}")

        # If no direct path provided, fall back to env vars
        if credentials_path is None:
            credentials_path = os.getenv(credentials_env)
        if database_url is None:
            database_url = os.getenv(url_env)

        if not credentials_path or not database_url:
            raise ValueError("Missing credentials path or database URL.")

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credential file not found at: {credentials_path}")

        cred = credentials.Certificate(credentials_path)
        app = firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        print("✅ Firebase initialized.")
        return db, app

    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return None, None

def RedXAIFirebaseTree(path=""):
    """
    Recursively lists all Firebase data from a given path.

    Args:
        path (str): Firebase path in bracket or slash format.

    Returns:
        Dict with full tree.
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")
    
    clean_path = path.replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(clean_path)
    data = ref.get()

    def walk(node, indent=0):
        if isinstance(node, dict):
            for k, v in node.items():
                print("  " * indent + f"📂 {k}/" if isinstance(v, dict) else "  " * indent + f"📄 {k}: {v}")
                walk(v, indent + 1)
        else:
            print("  " * indent + f"📄 {node}")

    print(f"🧭 Firebase Tree at: {clean_path or '/'}")
    walk(data)
    return data



def RedXAIFireAddKey(path, key, value):
    """
    Adds or updates a key:value pair to a Firebase path.

    Args:
        path (str): Path in bracket or slash format.
        key (str): Key name.
        value: Any Firebase-supported value.
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")
    clean_path = path.replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(clean_path)
    ref.update({key: value})
    print(f"➕ Added {key}: {value} at {clean_path}")

def RedXAIFireRemoveKey(path, key):
    """
    Removes a key from a Firebase value node (not the whole table).

    Args:
        path (str): Path to the node.
        key (str): Key to remove.
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")
    clean_path = path.replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(clean_path)
    ref.child(key).delete()
    print(f"🗑️ Removed key '{key}' from {clean_path}")



def RedXAIGoogleCloudInitialize(
    env_path=None,
    credentials_path=None,
    credentials_env="GCP_CREDENTIALS"
):
    """
    Initialize Google Cloud using a service account JSON.

    Supports:
    - Direct path
    - .env file with custom or default variable

    Args:
        env_path (str, optional): Path to the .env file to load.
        credentials_path (str, optional): Full path to GCP JSON file.
        credentials_env (str): Name of env var holding GCP JSON path.

    Returns:
        google.cloud.storage.Client or None
    """
    try:
        if env_path:
            load_dotenv(env_path)
            print(f"🔍 Loaded .env from: {env_path}")

        # Prioritize manual input, else use env var
        if not credentials_path:
            credentials_path = os.getenv(credentials_env)

        if not credentials_path:
            raise ValueError(f"Missing GCP credentials path. Make sure `{credentials_env}` is set in the .env.")

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"GCP credential file not found at: {credentials_path}")

        # Optional: Set for other Google libs
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Return any Google Cloud client (example: Storage)
        client = storage.Client.from_service_account_json(credentials_path)
        print("✅ Google Cloud initialized.")
        return client

    except Exception as e:
        print(f"❌ Google Cloud initialization failed: {e}")
        return None

def RedXAIFullInitialize(
    env_path=None,
    firebase_credentials_env="FIREBASE_CREDENTIALS",
    firebase_url_env="FIREBASE_DATABASE_URL",
    gcloud_credentials_env="GCP_CREDENTIALS"
):
    """
    Initializes Firebase and Google Cloud separately, each using different credentials.

    Args:
        env_path (str, optional): Path to .env file.
        firebase_credentials_env (str): Env var for Firebase JSON.
        firebase_url_env (str): Env var for Firebase DB URL.
        gcloud_credentials_env (str): Env var for GCP service account.

    Returns:
        (firebase_db, firebase_app, gcloud_client)
    """
    if env_path:
        load_dotenv(env_path)
        print(f"🔍 Loaded .env from: {env_path}")

    # Firebase init
    firebase_credentials_path = os.getenv(firebase_credentials_env)
    firebase_database_url = os.getenv(firebase_url_env)

    firebase_db, firebase_app = RedXAIFirebaseInitialize(
        credentials_path=firebase_credentials_path,
        database_url=firebase_database_url
    )

    # Google Cloud init (separate account)
    gcloud_credentials_path = os.getenv(gcloud_credentials_env)

    gcloud_client = RedXAIGoogleCloudInitialize(
        credentials_path=gcloud_credentials_path
    )

    return firebase_db, firebase_app, gcloud_client


# ✅ Add key/value flexibly
def RedXAIFireTableAdd(table_path, key=None, value=None):
    """
    Adds to a Firebase table at any depth using bracket path.
    - If key and value are provided: add/update key:value
    - If only key: creates key with 'Nil'
    - If only value: adds to a default key 'Value'
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")
    clean_path = table_path.replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(clean_path)

    if key and value is not None:
        ref.update({key: value})
        print(f"➕ Added {key}: {value} to {clean_path}")
    elif key and value is None:
        ref.update({key: "Nil"})
        print(f"➕ Added key '{key}' with default value to {clean_path}")
    elif value is not None and not key:
        ref.update({"Value": value})
        print(f"➕ Added value '{value}' under key 'Value' to {clean_path}")
    else:
        print("⚠️ Nothing to add. Provide key, value, or both.")

def RedXAIFireChange(db, table_path, new_value):
    """
    Example: RedXAIFireChange(db, "Table1[SubTable][SubSubTable]", {"new": "data"})
    """
    import re

    # Clean and split the path
    cleaned = re.findall(r'\w+', table_path)
    if not cleaned:
        raise ValueError("Invalid table path")

    ref = db.reference(cleaned[0])
    for key in cleaned[1:]:
        ref = ref.child(key)

    ref.set(new_value)


# ✅ Remove key or full table
def RedXAIFireTableRemove(table_path, key=None):
    """
    Removes a key or entire table.
    - If key is given: remove key from that table
    - If no key: remove the whole table at path
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")
    clean_path = table_path.replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(clean_path)

    if key:
        ref.child(key).delete()
        print(f"🗑️ Removed key '{key}' from {clean_path}")
    else:
        ref.delete()
        print(f"🗑️ Removed entire table at {clean_path}")

# ✅ Change value or entire table content
def RedXAIChangeFireTable(table_path, key=None, new_value=None):
    """
    Changes a key's value or replaces an entire table's value.
    - If key is provided: updates key's value inside the table
    - If no key: replaces the value of the table itself
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")
    clean_path = table_path.replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(clean_path)

    if key:
        ref.update({key: new_value})
        print(f"🔁 Changed {key} to {new_value} in {clean_path}")
    elif new_value is not None:
        ref.set(new_value)
        print(f"🔁 Replaced entire table at {clean_path} with value: {new_value}")
    else:
        print("⚠️ No key or value provided to change.")

# ✅ Search function
def RedXAIFireSearch(table_name_path="", key=None, value=None, detail_level="kv"):
    """
    Dynamically search Firebase Realtime DB for keys, values, or both.

    Args:
        table_name_path (str): Bracket-style path. "" = global search.
        key (str, optional): Key to match.
        value (any, optional): Value to match.
        detail_level (str):
            "k"    = key only
            "v"    = value only
            "kv"   = "key:value" string
            "kvp"  = return [key, value, path]
            "full" = return {"path": ..., "key": ..., "value": ...}

    Returns:
        List: Matching results.
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")

    def parse_path(path_str):
        if not path_str:
            return []
        return path_str.replace("][", "/").replace("[", "").replace("]", "").split("/")

    ref_path = parse_path(table_name_path)
    ref = db.reference("/".join(ref_path)) if ref_path else db.reference("/")
    data = ref.get()
    results = []

    def recursive_search(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                current_path = f"{path}/{k}" if path else k

                key_match = (key is None or k == key)
                value_match = (value is None or v == value)

                if key_match and value_match:
                    if detail_level == "k":
                        results.append(k)
                    elif detail_level == "v":
                        results.append(v)
                    elif detail_level == "kv":
                        results.append(f"{k}:{v}")
                    elif detail_level == "kvp":
                        results.append([k, v, current_path])
                    elif detail_level == "full":
                        results.append({"path": current_path, "key": k, "value": v})

                recursive_search(v, current_path)

        elif isinstance(node, list):
            for idx, item in enumerate(node):
                current_path = f"{path}/{idx}"
                if value is not None and item == value:
                    if detail_level == "k":
                        results.append(idx)
                    elif detail_level == "v":
                        results.append(item)
                    elif detail_level == "kv":
                        results.append(f"{idx}:{item}")
                    elif detail_level == "kvp":
                        results.append([idx, item, current_path])
                    elif detail_level == "full":
                        results.append({"path": current_path, "key": idx, "value": item})
                recursive_search(item, current_path)

    recursive_search(data)
    return results

def RedXAICloudCreateBucket(
    gcloud_client,
    bucket_name,
    main_folder=None,
    location="US",
    upload_file_path=None,
    destination_blob_name=None
):
    """
    Creates a new bucket. Optionally creates a main folder and uploads a file inside it.

    Args:
        gcloud_client: Google Cloud Storage client.
        bucket_name (str): Name of the bucket to create.
        main_folder (str, optional): Root folder to create inside the bucket.
        location (str): Bucket region (default: US).
        upload_file_path (str, optional): File to upload inside the folder.
        destination_blob_name (str, optional): Custom filename in bucket.

    Returns:
        storage.Bucket or None
    """
    try:
        bucket = gcloud_client.bucket(bucket_name)

        if bucket.exists():
            print(f"⚠️ Bucket '{bucket_name}' already exists.")
        else:
            bucket = gcloud_client.create_bucket(bucket, location=location)
            print(f"✅ Created bucket: {bucket.name} in {location}")

        # Create the main folder with a placeholder file
        if main_folder:
            blob = bucket.blob(f"{main_folder}/.folder")
            blob.upload_from_string("")  # empty file
            print(f"📁 Created folder: {main_folder}/")

        # Optional: Upload a file to the folder
        if upload_file_path:
            blob_name = destination_blob_name or os.path.basename(upload_file_path)
            full_path = f"{main_folder}/{blob_name}" if main_folder else blob_name
            blob = bucket.blob(full_path)
            blob.upload_from_filename(upload_file_path)
            print(f"📤 Uploaded '{upload_file_path}' as '{full_path}'")

        return bucket

    except Exception as e:
        print(f"❌ Failed to create bucket or upload: {e}")
        return None


def RedXAICloudCreateFolder(gcloud_client, bucket_name, folder_path):
    """
    Creates a folder (prefix) inside a Google Cloud Storage bucket.

    Args:
        gcloud_client: GCP storage client.
        bucket_name (str): Target bucket.
        folder_path (str): Folder path to create (e.g., 'user123/config').

    Returns:
        True if created successfully, False otherwise.
    """
    try:
        bucket = gcloud_client.bucket(bucket_name)
        folder_path = folder_path.rstrip("/") + "/"  # ensure trailing slash
        placeholder_blob = bucket.blob(f"{folder_path}.folder")
        placeholder_blob.upload_from_string("")
        print(f"📁 Folder created: {folder_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create folder '{folder_path}': {e}")
        return False



def RedXAICloudSearch(
    gcloud_client,
    search_path="",
    search_type="",  # "Bucket", "Folder", or "" (both)
    detail_level="full"  # "b", "f", "p", or "full"
):
    """
    Searches Google Cloud Storage like Firebase structure:
    - Global bucket search
    - Bucket/folder-level object search
    - Flexible detail levels

    Args:
        gcloud_client: Initialized GCP storage client.
        search_path (str): "" for all buckets or "bucket/folder/...".
        search_type (str): "Bucket", "Folder", or "" for both.
        detail_level (str): "b" = bucket, "f" = filename, "p" = full path, "full" = full metadata

    Returns:
        List of matching entries.
    """
    results = []

    try:
        if not search_path:
            # Global search: list buckets
            if search_type in ["Bucket", ""]:
                for bucket in gcloud_client.list_buckets():
                    if detail_level == "b":
                        results.append(bucket.name)
                    elif detail_level == "full":
                        results.append({
                            "name": bucket.name,
                            "location": bucket.location,
                            "created": bucket.time_created
                        })
            return results

        # Scoped path (must start with bucket name)
        parts = search_path.strip("/").split("/", 1)
        bucket_name = parts[0]
        folder_prefix = parts[1] if len(parts) > 1 else ""

        bucket = gcloud_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=folder_prefix)

        for blob in blobs:
            name = blob.name

            # If search_type is Folder, only include paths with slashes (folders or nested files)
            if search_type == "Folder" and "/" not in name.strip("/"):
                continue

            if detail_level == "b":
                results.append(bucket_name)
            elif detail_level == "f":
                results.append(os.path.basename(name))
            elif detail_level == "p":
                results.append(name)
            elif detail_level == "full":
                results.append({
                    "bucket": bucket_name,
                    "path": name,
                    "size": blob.size,
                    "updated": blob.updated,
                    "public_url": blob.public_url,
                })

        return results

    except Exception as e:
        print(f"❌ GCloud search failed: {e}")
        return []

def RedXAIDeleteBucket(gcloud_client, bucket_name, force=False):
    """
    Deletes a Google Cloud bucket.

    Args:
        gcloud_client: GCP storage client.
        bucket_name (str): Name of the bucket to delete.
        force (bool): If True, deletes all contents before deleting the bucket.

    Returns:
        True if deleted, False otherwise.
    """
    try:
        bucket = gcloud_client.bucket(bucket_name)

        if force:
            blobs = list(bucket.list_blobs())
            for blob in blobs:
                blob.delete()
                print(f"🗑️ Deleted: {blob.name}")

        bucket.delete(force=force)
        print(f"🪣 Deleted bucket: {bucket_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete bucket '{bucket_name}': {e}")
        return False
def RedXAICloudDeleteFolder(gcloud_client, bucket_name, folder_path):
    """
    Deletes a folder (prefix) and all its contents from a GCloud bucket.

    Args:
        gcloud_client: GCP storage client.
        bucket_name (str): Bucket name.
        folder_path (str): Folder path to delete (e.g., 'user123/data').

    Returns:
        Number of deleted files.
    """
    try:
        bucket = gcloud_client.bucket(bucket_name)
        folder_path = folder_path.rstrip("/") + "/"  # ensure trailing slash
        blobs = bucket.list_blobs(prefix=folder_path)
        count = 0

        for blob in blobs:
            blob.delete()
            print(f"🗑️ Deleted: {blob.name}")
            count += 1

        print(f"🧹 Folder '{folder_path}' deleted ({count} items).")
        return count
    except Exception as e:
        print(f"❌ Failed to delete folder '{folder_path}': {e}")
        return 0

import os

def RedXAICloudUpload(path, file_or_folder, gcloud_client):
    """
    Uploads a file or folder to a Google Cloud bucket.

    Args:
        path (str): Destination path in format "bucket_name/optional/folder".
        file_or_folder (str): Local file or folder path to upload.
        gcloud_client: GCP storage client.

    Returns:
        True if successful, False otherwise.
    """
    try:
        path = path.strip("/")
        parts = path.split("/", 1)
        bucket_name = parts[0]
        target_prefix = parts[1] if len(parts) > 1 else ""

        bucket = gcloud_client.bucket(bucket_name)

        if os.path.isfile(file_or_folder):
            filename = os.path.basename(file_or_folder)
            blob_path = f"{target_prefix}/{filename}" if target_prefix else filename
            bucket.blob(blob_path).upload_from_filename(file_or_folder)
            print(f"📤 Uploaded file: {blob_path}")
        elif os.path.isdir(file_or_folder):
            for root, _, files in os.walk(file_or_folder):
                for f in files:
                    full_path = os.path.join(root, f)
                    relative_path = os.path.relpath(full_path, file_or_folder)
                    blob_path = f"{target_prefix}/{relative_path}".replace("\\", "/")
                    bucket.blob(blob_path).upload_from_filename(full_path)
                    print(f"📤 Uploaded: {blob_path}")
        else:
            print("⚠️ File or folder not found.")
            return False

        return True

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

def RedXAICloudRemoveFile(gcloud_client, path):
    """
    Removes a file from Google Cloud using full path.

    Args:
        gcloud_client: Google Cloud Storage client.
        path (str): "bucket_name/file.txt" or "bucket_name/folder/file.txt"
    """
    try:
        parts = path.strip("/").split("/", 1)
        bucket_name = parts[0]
        blob_path = parts[1] if len(parts) > 1 else ""

        bucket = gcloud_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        if not blob.exists():
            print(f"⚠️ File does not exist: {blob_path}")
            return False

        blob.delete()
        print(f"🗑️ Deleted file: {blob_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete file: {e}")
        return False




def RedXAICloudTree(gcloud_client, path=""):
    """
    Recursively lists files inside a GCloud bucket or folder.

    Args:
        gcloud_client: GCP client
        path (str): "bucket", or "bucket/folder"

    Returns:
        List of full blob paths
    """
    try:
        path = path.strip("/")
        parts = path.split("/", 1)
        bucket_name = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""

        bucket = gcloud_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        print(f"🧭 GCloud Tree: gs://{bucket_name}/{prefix}")
        blob_paths = []

        for blob in blobs:
            print(f"📄 {blob.name}")
            blob_paths.append(blob.name)

        return blob_paths
    except Exception as e:
        print(f"❌ Failed to list GCloud tree: {e}")
        return []

import requests
from firebase_admin import db
import firebase_admin

def RedXAIServerExchange(
    endpoint_path,
    data=None,
    method="POST",
    cloud_run_url=None,
    firebase_root="ServerExchange"
):
    """
    Smart server-side data exchange using Firebase or Cloud Run.

    Args:
        endpoint_path (str): Firebase key path or Cloud Run route (e.g. "user/message").
        data (dict or single value): Data to send.
        method (str): HTTP method if Cloud Run is used.
        cloud_run_url (str, optional): Full Cloud Run base URL (e.g. https://your-api.run.app)
        firebase_root (str): Firebase root node to write to (default: ServerExchange)

    Returns:
        Response data (dict, string, etc.) or None
    """
    # Format data
    payload = data
    if not isinstance(payload, (dict, list, str, int, float, bool)):
        print("⚠️ Invalid payload type.")
        return None

    # ✅ Case 1: Use Firebase if it's initialized
    if firebase_admin._apps:
        try:
            clean_path = endpoint_path.replace("][", "/").replace("[", "").replace("]", "")
            ref = db.reference(f"{firebase_root}/{clean_path}")
            ref.set(payload)
            response = ref.get()
            print(f"📡 Sent via Firebase to: {firebase_root}/{clean_path}")
            return response
        except Exception as e:
            print(f"❌ Firebase exchange failed: {e}")

    # ✅ Case 2: Use Cloud Run if Firebase isn't available or fails
    if cloud_run_url:
        try:
            url = f"{cloud_run_url.rstrip('/')}/{endpoint_path.lstrip('/')}"
            headers = {"Content-Type": "application/json"}
            method = method.upper()
            if method == "POST":
                res = requests.post(url, json=payload, headers=headers)
            elif method == "GET":
                res = requests.get(url, params=payload if isinstance(payload, dict) else {}, headers=headers)
            else:
                print("⚠️ Unsupported HTTP method.")
                return None

            if res.ok:
                print(f"📡 Sent via Cloud Run → {url}")
                return res.json() if "application/json" in res.headers.get("Content-Type", "") else res.text
            else:
                print(f"❌ Cloud Run error: {res.status_code} {res.text}")
        except Exception as e:
            print(f"❌ Cloud Run request failed: {e}")

    print("⚠️ No valid backend available (Firebase or Cloud Run).")
    return None



import requests
from firebase_admin import db
import firebase_admin

def RedXAIReceiveFromServer(
    user_key,
    cloud_run_url=None,
    firebase_root="ServerExchange",
    path_suffix=""
):
    """
    Smart receive from Firebase or Cloud Run using user_key.

    Args:
        user_key (str): Key to pull data for (e.g., user ID, session ID).
        cloud_run_url (str, optional): Cloud Run endpoint.
        firebase_root (str): Firebase node to listen to.
        path_suffix (str): Optional trailing path (e.g., "/game", "/message")

    Returns:
        Received data (dict, str, etc.) or None
    """
    try:
        # ✅ Try Firebase if initialized
        if firebase_admin._apps:
            full_path = f"{firebase_root}/{user_key}"
            if path_suffix:
                full_path += f"/{path_suffix.strip('/')}"
            clean_path = full_path.replace("][", "/").replace("[", "").replace("]", "")
            ref = db.reference(clean_path)
            data = ref.get()
            print(f"📥 Pulled from Firebase: {clean_path}")
            return data

        # ✅ If not, try Cloud Run
        if cloud_run_url:
            full_url = f"{cloud_run_url.rstrip('/')}/receive/{user_key}"
            if path_suffix:
                full_url += f"/{path_suffix.strip('/')}"
            res = requests.get(full_url)
            if res.ok:
                print(f"📥 Pulled from Cloud Run: {full_url}")
                return res.json() if "application/json" in res.headers.get("Content-Type", "") else res.text
            else:
                print(f"❌ Cloud Run returned error: {res.status_code}")
    except Exception as e:
        print(f"❌ Receive failed: {e}")

    print("⚠️ No data source available.")
    return None


from firebase_admin import db
import firebase_admin

def RedXAISendFirebase(path, data, firebase_root="ServerExchange"):
    """
    Explicitly sends data to Firebase Realtime Database only.

    Args:
        path (str): Firebase key path (e.g. "user123/game").
        data (any): Supported Firebase value (dict, str, number, etc.)
        firebase_root (str): Root node to send into.
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase is not initialized.")
    
    full_path = f"{firebase_root}/{path}".replace("][", "/").replace("[", "").replace("]", "")
    ref = db.reference(full_path)
    ref.set(data)
    print(f"📤 Sent via Firebase: {full_path}")
    return True


import requests

def RedXAISendCloudRun(
    cloud_run_url,
    endpoint_path,
    data,
    method="POST"
):
    """
    Explicitly sends data to a Google Cloud Run endpoint.

    Args:
        cloud_run_url (str): Base Cloud Run URL (e.g. https://api-xyz.a.run.app)
        endpoint_path (str): Endpoint path (e.g. "game/update")
        data (any): Data to send (dict, string, number, etc.)
        method (str): HTTP method (POST/GET)

    Returns:
        Parsed response or None
    """
    try:
        url = f"{cloud_run_url.rstrip('/')}/{endpoint_path.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        method = method.upper()

        if method == "POST":
            res = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            res = requests.get(url, params=data if isinstance(data, dict) else {}, headers=headers)
        else:
            print("⚠️ Invalid method")
            return None

        if res.ok:
            print(f"📤 Sent via Cloud Run → {url}")
            return res.json() if "application/json" in res.headers.get("Content-Type", "") else res.text
        else:
            print(f"❌ Cloud Run Error: {res.status_code}")
            return None

    except Exception as e:
        print(f"❌ Failed to send via Cloud Run: {e}")
        return None



import os

def RedXAICloudDownload(path, output_folder, gcloud_client):
    """
    Downloads a file, folder, or full bucket from Google Cloud Storage.

    Args:
        path (str): "bucket" or "bucket/folder" or "bucket/file.ext"
        output_folder (str): Local folder to save files into
        gcloud_client: GCP storage client

    Returns:
        List of downloaded files
    """
    try:
        path = path.strip("/")
        parts = path.split("/", 1)
        bucket_name = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""

        bucket = gcloud_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        downloaded = []
        for blob in blobs:
            relative_path = blob.name[len(prefix):].lstrip("/") if prefix else blob.name
            local_path = os.path.join(output_folder, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            blob.download_to_filename(local_path)
            print(f"⬇️ Downloaded: {blob.name} → {local_path}")
            downloaded.append(local_path)

        return downloaded

    except Exception as e:
        print(f"❌ Download failed: {e}")
        return []



def RedXAIExportFirebaseTree(output_file="firebase_tree.txt"):
    """
    Exports the entire Firebase database as a readable tree into a text file.
    """
    if not firebase_admin._apps:
        raise RuntimeError("Firebase not initialized.")

    ref = db.reference("/")
    data = ref.get()

    def write_tree(node, indent=0, lines=None):
        if lines is None:
            lines = []

        if isinstance(node, dict):
            for key, val in node.items():
                lines.append("  " * indent + f"📂 {key}/" if isinstance(val, dict) else "  " * indent + f"📄 {key}: {val}")
                write_tree(val, indent + 1, lines)
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                lines.append("  " * indent + f"[{idx}]: {item}")
        return lines

    try:
        lines = write_tree(data)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"📝 Firebase exported to: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Firebase export failed: {e}")
        return None



def RedXAIExportCloudTree(gcloud_client, path="", output_file="cloud_tree.txt"):
    """
    Exports GCloud Storage bucket/folder structure to a text file.

    Args:
        gcloud_client: GCP client
        path (str): "bucket" or "bucket/folder"
        output_file (str): Local file to write tree

    Returns:
        File path written to
    """
    try:
        parts = path.strip("/").split("/", 1)
        bucket_name = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""

        bucket = gcloud_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        lines = [f"🪣 Bucket: {bucket_name}"]
        for blob in blobs:
            lines.append(f"📄 {blob.name}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"📝 Cloud tree exported to: {output_file}")
        return output_file

    except Exception as e:
        print(f"❌ Cloud export failed: {e}")
        return None


def RedXAIExportAll(output_dir, gcloud_client):
    """
    Exports both Firebase and Cloud Storage trees into one folder.

    Args:
        output_dir (str): Local folder to save both exports.
        gcloud_client: GCP client

    Returns:
        Tuple of both file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    fb_path = os.path.join(output_dir, "firebase_tree.txt")
    cloud_path = os.path.join(output_dir, "cloud_tree.txt")

    RedXAIExportFirebaseTree(fb_path)
    RedXAIExportCloudTree(gcloud_client, "", cloud_path)
    print(f"✅ All data exported to: {output_dir}")
    return fb_path, cloud_path


