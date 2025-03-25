from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..models.transcriptions import Transcription


class TranscriptionsAPI:
    """API endpoints for transcriptions."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("TranscriptionsAPI initialized")

    async def list(
        self,
        from_date: str,
        to_date: str,
        meeting_uuid: Optional[UUID] = None,
    ) -> List[Transcription]:
        """List transcriptions with optional filters.

        Args:
            from_date: Start date-time in ISO format
            to_date: End date-time in ISO format
            meeting_uuid: Optional meeting UUID to filter by

        Returns:
            List of transcriptions
        """
        self.client.logger.debug(
            f"Listing transcriptions from {from_date} to {to_date}"
        )
        if meeting_uuid:
            self.client.logger.debug(f"Filtering by meeting UUID: {meeting_uuid}")

        params = {
            "from_date": from_date,
            "to_date": to_date,
        }

        if meeting_uuid is not None:
            params["meeting_uuid"] = str(meeting_uuid)

        data = await self.client._request("GET", "/transcriptions", params=params)
        transcriptions = [Transcription.model_validate(item) for item in data]
        self.client.logger.debug(f"Retrieved {len(transcriptions)} transcriptions")
        return transcriptions

    async def get(self, uuid: UUID) -> Transcription:
        """Get a single transcription by UUID.

        Args:
            uuid: Transcription UUID

        Returns:
            Transcription details
        """
        self.client.logger.debug(f"Getting transcription with UUID: {uuid}")
        data = await self.client._request("GET", f"/transcriptions/{uuid}")
        transcription = Transcription.model_validate(data)
        self.client.logger.debug(f"Retrieved transcription: {uuid}")
        return transcription

    async def get_by_meeting_id(self, meeting_id: UUID) -> Optional[Transcription]:
        """Get transcription for a specific meeting by ID.

        This method first tries to get transcriptions filtered by meeting_uuid.
        If no transcription is found, it checks the meeting details to see if a
        transcription_uuid is available, and attempts to fetch by that UUID.

        Args:
            meeting_id: UUID of the meeting

        Returns:
            Transcription if available, None otherwise
        """
        self.client.logger.debug(f"Getting transcription for meeting: {meeting_id}")

        # First try to get transcriptions filtered by meeting_uuid
        params = {"meeting_uuid": str(meeting_id)}
        try:
            data = await self.client._request("GET", "/transcriptions", params=params)

            # Handle list responses
            if isinstance(data, list):
                if data:
                    transcription = Transcription.model_validate(data[0])
                    self.client.logger.debug(
                        f"Retrieved transcription for meeting: {meeting_id}"
                    )
                    return transcription
                else:
                    self.client.logger.debug(
                        f"No transcriptions found for meeting: {meeting_id}"
                    )

            # Handle dict with results
            elif isinstance(data, dict) and "results" in data:
                results = data.get("results", [])
                if results:
                    transcription = Transcription.model_validate(results[0])
                    self.client.logger.debug(
                        f"Retrieved transcription from results for meeting: {meeting_id}"
                    )
                    return transcription
                else:
                    self.client.logger.debug(
                        f"No transcriptions found in results for meeting: {meeting_id}"
                    )

        except Exception as e:
            self.client.logger.debug(f"Error getting transcriptions by meeting ID: {e}")

        # If no transcription found, check the meeting to see if it has a transcription_uuid
        try:
            meeting_data = await self.client._request("GET", f"/meetings/{meeting_id}")

            transcription_uuid = meeting_data.get("transcription_uuid")
            if transcription_uuid:
                self.client.logger.debug(
                    f"Found transcription UUID {transcription_uuid} in meeting details"
                )

                # Try to get the specific transcription
                try:
                    data = await self.client._request(
                        "GET", f"/transcriptions/{transcription_uuid}"
                    )
                    transcription = Transcription.model_validate(data)
                    self.client.logger.debug(
                        f"Retrieved transcription by UUID from meeting: {transcription_uuid}"
                    )
                    return transcription
                except Exception as e:
                    self.client.logger.debug(
                        f"Error getting transcription by UUID from meeting: {e}"
                    )
        except Exception as e:
            self.client.logger.debug(f"Error getting meeting details: {e}")

        self.client.logger.debug(
            f"Could not find any transcription for meeting: {meeting_id}"
        )
        return None
