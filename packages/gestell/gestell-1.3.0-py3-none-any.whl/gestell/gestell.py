import os
from typing import AsyncGenerator, List, Literal, Optional, Union
from dotenv import load_dotenv
from gestell.document.export import ExportDocumentRequest, export_document
from gestell.document.upload import (
    UploadDocumentRequest,
    UploadDocumentResponse,
    upload_document,
)
from gestell.organization.get import (
    get_organization,
    GetOrganizationRequest,
    GetOrganizationResponse,
)
from gestell.organization.list import (
    list_organizations,
    GetOrganizationsRequest,
    GetOrganizationsResponse,
)
from gestell.organization.update import (
    update_organization,
    UpdateOrganizationRequest,
    UpdateOrganizationResponse,
)
from gestell.organization.members.add import (
    add_members,
    AddMembersRequest,
    AddMembersResponse,
)
from gestell.organization.members.remove import (
    remove_members,
    RemoveMembersRequest,
    RemoveMembersResponse,
)
from gestell.collection.get import (
    get_collection,
    GetCollectionRequest,
    GetCollectionResponse,
)
from gestell.collection.list import (
    list_collections,
    GetCollectionsRequest,
    GetCollectionsResponse,
)
from gestell.collection.create import (
    create_collection,
    CreateCollectionRequest,
    CreateCollectionResponse,
)
from gestell.collection.update import (
    UpdateCollectionRequest,
    UpdateCollectionResponse,
    update_collection,
)
from gestell.collection.delete import (
    DeleteCollectionRequest,
    delete_collection,
)
from gestell.collection.addCategory import (
    add_category,
    AddCategoryRequest,
    AddCategoryResponse,
)
from gestell.collection.updateCategory import (
    UpdateCategoryRequest,
    UpdateCategoryResponse,
    update_category,
)
from gestell.collection.removeCategory import (
    RemoveCategoryRequest,
    RemoveCategoryResponse,
    remove_category,
)
from gestell.query.exportFeatures import ExportFeaturesRequest, export_features
from gestell.query.exportTable import ExportTableRequest, export_table
from gestell.query.search import (
    search_query,
    SearchQueryRequest,
    SearchQueryResponse,
)
from gestell.query.prompt import (
    PromptMessage,
    PromptQueryRequest,
    prompt_query,
)
from gestell.query.features import (
    featuresQuery,
    FeaturesQueryRequest,
    FeaturesQueryResponse,
)
from gestell.query.table import (
    TablesQueryRequest,
    tables_query,
    TablesQueryResponse,
)
from gestell.document.get import (
    GetDocumentResponse,
    GetDocumentRequest,
    get_document,
)
from gestell.document.list import (
    GetDocumentsRequest,
    GetDocumentsResponse,
    list_documents,
)
from gestell.document.presign import (
    PresignDocumentRequest,
    PresignDocumentResponse,
    presign_document,
)
from gestell.document.create import (
    CreateDocumentRequest,
    CreateDocumentResponse,
    create_document,
)
from gestell.document.update import (
    update_document,
    UpdateDocumentRequest,
)
from gestell.document.delete import (
    delete_document,
    DeleteDocumentRequest,
)
from gestell.job.get import (
    GetJobRequest,
    get_job,
    GetJobResponse,
)
from gestell.job.list import (
    list_jobs,
    GetJobsRequest,
    GetJobsResponse,
)
from gestell.job.reprocess import (
    reprocess_document,
    ReprocessDocumentsRequest,
    ReprocessDocumentsResponse,
)
from gestell.job.cancel import (
    cancel_jobs,
    CancelJobsRequest,
    CancelJobsResponse,
)
from gestell.types import (
    BaseResponse,
    OrganizationMemberPayload,
    CollectionType,
    CategoryType,
    CreateCategoryPayload,
    JobStatusType,
    SearchMethod,
    SearchType,
    JobType,
)


class Gestell:
    """
    The Gestell SDK Instance
    """

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        debug: Optional[bool] = False,
    ):
        """
        Initializes the Gestell instance.

        @param `url`: The API URL, defaults to `GESTELL_API_URL` or https://platform.gestell.ai
        @param `key`: The API Key, defaults to `GESTELL_API_KEY` in the terminal session
        @param `debug`: More verbose error outputs
        """
        load_dotenv()

        self.api_url: str = url or os.getenv(
            'GESTELL_API_URL', 'https://platform.gestell.ai'
        )
        self.api_key: str = key or os.getenv('GESTELL_API_KEY', '')
        self.debug: bool = debug or False

    @property
    def organization(self):
        """
        Manages organizations you are a part of.
        Learn more about usage at: https://gestell.ai/docs/reference#organization
        """
        return self.__Organization__(self)

    @property
    def collection(self):
        """
        Manage collections you are a part of.
        Learn more about usage at: https://gestell.ai/docs/reference#collection
        """
        return self.__Collection__(self)

    @property
    def query(self):
        """
        Query a collection. This requires your collection ID to query
        Note that querying tables and features requires both a collection_id and category_id.
        Learn more about usage at: https://gestell.ai/docs/reference#query
        """
        return self.__Query__(self)

    @property
    def document(self):
        """
        Manage documents within a collection. You will need to retrieve the collection id to manage documents.
        Learn more about usage at: https://gestell.ai/docs/reference#document

        @param collection_id - The ID of the collection
        @param document_id - The ID of the document, this is usually required unless creating a document
        """
        return self.__Document__(self)

    @property
    def job(self):
        """
        Manage jobs within a collection. You will need to retrieve the collection id to manage jobs.
        Learn more about usage at: https://gestell.ai/docs/reference#job

        @param collection_id - The ID of the collection
        """
        return self.__Job__(self)

    class __Organization__:
        """
        Manages organizations you are a part of.
        Learn more about usage at: https://gestell.ai/docs/reference#organization
        """

        def __init__(self, parent: 'Gestell'):
            self.parent = parent

        async def get(self, id: str) -> GetOrganizationResponse:
            """
            Fetches the details of a specific organization using its unique ID.
            Learn more about usage at: https://gestell.ai/docs/reference#organization

            @param `id`: The ID of the organization to retrieve.
            @returns A dictionary containing organization details, including:
                      - `id`: The unique identifier of the organization.
                      - `name`: The name of the organization.
                      - `description`: A brief description of the organization.
                      - `members`: An array of members belonging to the organization.
                      - `collections`: An array of collections associated with the organization.
                      - `dateCreated`: The date the organization was created.
                      - `dateUpdated`: The date the organization was last updated.
            """
            request = GetOrganizationRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=id,
            )
            response: GetOrganizationResponse = await get_organization(request)
            return response

        async def list(
            self,
            search: Optional[str] = None,
            take: Optional[int] = 10,
            skip: Optional[int] = 0,
            extended: Optional[bool] = None,
        ) -> GetOrganizationsResponse:
            """
            Fetches a list of organizations that the user is associated with, with optional filters or pagination parameters.
            Learn more about usage at: https://gestell.ai/docs/reference#organization

            @param `payload`: - Optional parameters for filtering or pagination, including:
            - `search`: A search query to filter organizations by name or description.
            - `take`: The number of organizations to retrieve.
            - `skip`: The number of organizations to skip (useful for pagination).
            - `extended`: Whether to include extended details for each organization.
            returns A promise that resolves to an array of organization details, where each organization includes:
            - `id`: The unique identifier of the organization.
            - `name`: The name of the organization.
            - `description`: A brief description of the organization.
            - `members`: An optional array of members belonging to the organization.
            - `collections`: An optional array of collections associated with the organization.
            - `dateCreated`: The date the organization was created.
            - `dateUpdated`: The date the organization was last updated.
            """
            request = GetOrganizationsRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                search=search,
                take=take,
                skip=skip,
                extended=extended,
            )
            response: GetOrganizationsResponse = await list_organizations(request)
            return response

        async def update(
            self,
            id: str,
            name: str,
            description: str,
        ) -> UpdateOrganizationResponse:
            """
            Allows updating the details of an existing organization. Requires the organization ID and the updated information in the payload.
            Learn more about usage at: https://gestell.ai/docs/reference#organization

            @param `payload`: - The details of the organization to update, including:
            - `id`: The unique identifier of the organization to update.
            - `name`: The updated name of the organization.
            - `description`: The updated description of the organization.
            returns A promise that resolves to the response of the update request, including:
            - `status`: The status of the update request.
            - `message`: An optional message providing additional details about the request result.
            """
            request = UpdateOrganizationRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=id,
                name=name,
                description=description,
            )
            response: UpdateOrganizationResponse = await update_organization(request)
            return response

        async def add_members(
            self, id: str, members: List[OrganizationMemberPayload]
        ) -> BaseResponse:
            """
            Adds new members to the organization based on the provided payload.
            Learn more about usage at: https://gestell.ai/docs/reference#organization

            @param `payload`: - The details of the members to add, including:
            - `id`: The id of the organization
            - `members`: An array of the members which include the following:
                - `id`: The identifier of the member to add, which can be a UUID or an email.
                - `role`: The role of the member within the organization, either `member` or `admin`.
            returns A promise that resolves to the response of the add member request, including:
            - `status`: The status of the add request.
            - `message`: An optional message providing additional details about the request result.
            """
            request = AddMembersRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=id,
                members=members,
            )
            response: AddMembersResponse = await add_members(request)
            return response

        async def remove_members(self, id: str, members: List[str]) -> BaseResponse:
            """
            Removes existing members from the organization based on the provided payload.
            Learn more about usage at: https://gestell.ai/docs/reference#organization

            @param payload - The details of the members to remove:
            - `id`: The id of the organization
            - `members`: The identifier of the member to remove, which can be a UUID or an email.
            returns A promise that resolves to the response of the remove member request, including:
            - `status`: The status of the remove request.
            - `message`: An optional message providing additional details about the request result.
            """
            request = RemoveMembersRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=id,
                members=members,
            )
            response: RemoveMembersResponse = await remove_members(request)
            return response

    class __Collection__:
        """
        Manages collections you are a part of.
        Learn more about usage at: https://gestell.ai/docs/reference#collection
        """

        def __init__(self, parent: 'Gestell'):
            self.parent = parent

        async def get(self, collection_id: str) -> GetCollectionResponse:
            """
            Fetches the details of a specific collection using its unique ID.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param collection_id - The ID of the collection to retrieve.
            returns A promise that resolves to the collection details, including:
             - `result`: The details of the collection, or `null` if not found. The collection includes:
               - `id`: The unique identifier of the collection.
               - `organizationId`: The ID of the organization that owns the collection.
               - `organization`: The organization associated with the collection.
               - `name`: The name of the collection.
               - `type`: The type of the collection (`frame`, `searchable-frame`, `canon`, or `features`).
               - `description`: A brief description of the collection.
               - `tags`: An array of tags associated with the collection.
               - `instructions`: Optional general instructions for the collection.
               - `graphInstructions`: Optional graph-specific instructions for the collection.
               - `promptInstructions`: Optional prompt-specific instructions for the collection.
               - `searchInstructions`: Optional search-specific instructions for the collection.
               - `categories`: An optional array of categories included in the collection.
               - `documents`: An optional array of documents associated with the collection.
               - `dateCreated`: The date the collection was created.
               - `dateUpdated`: The date the collection was last updated.
             - `stats`: The statistics of the collection, or `null` if unavailable. The stats include:
               - `docs`: The total number of documents in the collection.
               - `size`: The total size of the collection.
               - `nodes`: The number of nodes in the collection.
               - `status`: An object representing the status of the collection, including:
                 - `documents`: The number of documents processed.
                 - `nodes`: The number of nodes processed.
                 - `edges`: The number of edges processed.
                 - `vectors`: The number of vectors processed.
                 - `category`: The number of categories processed.
             - `status`: The status of the fetch request.
             - `message`: An optional message providing additional details about the request result.
            """
            request = GetCollectionRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
            )
            response: GetCollectionResponse = await get_collection(request)
            return response

        async def list(
            self,
            search: Optional[str] = None,
            take: Optional[int] = 10,
            skip: Optional[int] = 0,
            extended: Optional[bool] = None,
        ) -> GetCollectionsResponse:
            """
            Fetches a list of collections, with optional filters or pagination parameters.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param payload - Optional parameters for filtering or pagination, including:
            - `search`: A search query to filter collections by name, description, or tags.
            - `take`: The number of collections to retrieve.
            - `skip`: The number of collections to skip (useful for pagination).
            - `extended`: Whether to include extended details for each collection.
            returns A promise that resolves to an array of collections, where each collection includes:
            - `id`: The unique identifier of the collection.
            - `organizationId`: The ID of the organization that owns the collection.
            - `organization`: The organization associated with the collection.
            - `name`: The name of the collection.
            - `type`: The type of the collection (`frame`, `searchable-frame`, `canon`, or `features`).
            - `description`: A brief description of the collection.
            - `tags`: An array of tags associated with the collection.
            - `instructions`: Optional general instructions for the collection.
            - `graphInstructions`: Optional graph-specific instructions for the collection.
            - `promptInstructions`: Optional prompt-specific instructions for the collection.
            - `searchInstructions`: Optional search-specific instructions for the collection.
            - `categories`: An optional array of categories included in the collection.
            - `documents`: An optional array of documents associated with the collection.
            - `dateCreated`: The date the collection was created.
            - `dateUpdated`: The date the collection was last updated.
            """
            request = GetCollectionsRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                search=search,
                take=take,
                skip=skip,
                extended=extended,
            )
            response: GetCollectionsResponse = await list_collections(request)
            return response

        async def create(
            self,
            organization_id: str,
            name: str,
            type: CollectionType,
            tags: Optional[List[str]] = None,
            description: Optional[str] = None,
            instructions: Optional[str] = None,
            graphInstructions: Optional[str] = None,
            promptInstructions: Optional[str] = None,
            searchInstructions: Optional[str] = None,
            categories: Optional[List[CreateCategoryPayload]] = None,
        ) -> CreateCollectionResponse:
            """
            Allows the creation of a new collection by providing the required details in the payload.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param payload - The details of the new collection to create, including:
            - `organization_id`: The ID of the organization to which the collection belongs.
            - `name`: The name of the collection.
            - `type`: The type of the collection (`frame`, `searchable-frame`, `canon`, or `features`).
            - `tags`: An optional array of tags associated with the collection.
            - `description`: An optional description of the collection.
            - `instructions`: Optional general instructions for the collection.
            - `graphInstructions`: Optional graph-specific instructions for the collection.
            - `promptInstructions`: Optional prompt-specific instructions for the collection.
            - `searchInstructions`: Optional search-specific instructions for the collection.
            - `categories`: An optional array of categories to associate with the collection. Each category includes:
            - `name`: The name of the category.
            - `type`: The type of the category.
            - `instructions`: The instructions for the category.
            returns A promise that resolves to the response of the collection creation request, including:
            - `status`: The status of the creation request.
            - `message`: An optional message providing additional details about the request result.
            - `id`: The unique identifier of the newly created collection.
            """
            request = CreateCollectionRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                organization_id=organization_id,
                name=name,
                type=type,
                tags=tags,
                description=description,
                instructions=instructions,
                graphInstructions=graphInstructions,
                promptInstructions=promptInstructions,
                searchInstructions=searchInstructions,
                categories=categories,
            )
            response: CreateCollectionResponse = await create_collection(request)
            return response

        async def update(
            self,
            collection_id: str,
            organization_id: Optional[str] = None,
            name: Optional[str] = None,
            type: Optional[CollectionType] = None,
            description: Optional[str] = None,
            instructions: Optional[str] = None,
            graphInstructions: Optional[str] = None,
            promptInstructions: Optional[str] = None,
            searchInstructions: Optional[str] = None,
            tags: Optional[List[str]] = None,
        ) -> UpdateCollectionResponse:
            """
            Allows the update of an existing collection by providing the necessary details in the payload.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param payload - The details of the collection to update, including:
            - `id`: The unique identifier of the collection to update.
            - `organization_id`: An optional update for the organization ID associated with the collection.
            - `name`: An optional new name for the collection.
            - `type`: An optional new type for the collection (`frame`, `searchable-frame`, `canon`, or `features`).
            - `description`: An optional new description for the collection.
            - `instructions`: Optional general instructions for the collection.
            - `graphInstructions`: Optional graph-specific instructions for the collection.
            - `promptInstructions`: Optional prompt-specific instructions for the collection.
            - `searchInstructions`: Optional search-specific instructions for the collection.
            - `tags`: An optional array of new tags to associate with the collection.
            @returns A promise that resolves to the response of the collection update request, including:
            - `status`: The status of the update request.
            - `message`: An optional message providing additional details about the request result.
            """
            request = UpdateCollectionRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                organization_id=organization_id,
                name=name,
                type=type,
                description=description,
                instructions=instructions,
                graphInstructions=graphInstructions,
                promptInstructions=promptInstructions,
                searchInstructions=searchInstructions,
                tags=tags,
            )
            response: UpdateCollectionResponse = await update_collection(request)
            return response

        async def delete(self, collection_id: str) -> BaseResponse:
            """
            Deletes an existing collection based on its unique ID.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param collection_id - The ID of the collection to delete.
            @returns A promise that resolves to the response of the collection update request, including:
            - `status`: The status of the update request.
            - `message`: An optional message providing additional details about the request result.
            """
            request = DeleteCollectionRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
            )
            response: BaseResponse = await delete_collection(request)
            return response

        async def add_category(
            self,
            collection_id: str,
            name: str,
            type: str,
            instructions: str,
        ) -> AddCategoryResponse:
            """
            Adds a new category to an existing collection.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param payload - The details of the category to add, including:
            - `collection_id`: The ID of the collection to which the category will be added.
            - `name`: The name of the new category.
            - `type`: The type of the category (e.g., custom or predefined).
            - `instructions`: Additional instructions or notes related to the category.

            @returns A promise that resolves to the response of the category addition, including:
            - `status`: The status of the request (`OK` or `ERROR`).
            - `message`: An optional message providing additional details about the request result.
            - `id`: The unique identifier of the newly added category.
            """
            request = AddCategoryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                name=name,
                type=type,
                instructions=instructions,
            )
            response: AddCategoryResponse = await add_category(request)
            return response

        async def update_category(
            self,
            collection_id: str,
            category_id: str,
            name: Optional[str] = None,
            type: Optional[CategoryType] = None,
            instructions: Optional[str] = None,
        ) -> UpdateCategoryResponse:
            """
            Updates an existing category within a collection.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param payload - The details of the category to update, including:
            - `collection_id`: The ID of the collection containing the category.
            - `category_id`: The unique identifier of the category to update.
            - `name`: (Optional) The updated name of the category.
            - `type`: (Optional) The updated type of the category (e.g., custom or predefined).
            - `instructions`: (Optional) Additional updated instructions or notes related to the category.

            @returns A promise that resolves to the response of the category update, including:
            - `status`: The status of the request (`OK` or `ERROR`).
            - `message`: An optional message providing additional details about the request result.
            """
            request = UpdateCategoryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                name=name,
                type=type,
                instructions=instructions,
            )
            response: UpdateCategoryResponse = await update_category(request)
            return response

        async def remove_category(
            self, collection_id: str, category_id: str
        ) -> RemoveCategoryResponse:
            """
            Removes an existing category from a collection.
            Learn more about usage at: https://gestell.ai/docs/reference#collection

            @param payload - The details of the category to remove, including:
            - `collection_id`: The ID of the collection containing the category.
            - `category_id`: The unique identifier of the category to remove.

            @returns A promise that resolves to the response of the category removal, including:
            - `status`: The status of the request (`OK` or `ERROR`).
            - `message`: An optional message providing additional details about the request result.
            """
            request = RemoveCategoryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
            )
            response: RemoveCategoryResponse = await remove_category(request)
            return response

    class __Query__:
        """
        Query a collection. This requires your collection ID to query
        Note that querying tables and features requires both a collection_id and category_id.
        Learn more about usage at: https://gestell.ai/docs/reference#query
        """

        def __init__(self, parent: 'Gestell'):
            self.parent = parent

        async def search(
            self,
            collection_id: str,
            prompt: str,
            category_id: Optional[str] = None,
            method: Optional[SearchMethod] = None,
            type: Optional[SearchType] = None,
            vectorDepth: Optional[int] = None,
            nodeDepth: Optional[int] = None,
            maxQueries: Optional[int] = None,
            maxResults: Optional[int] = None,
            includeContent: Optional[bool] = None,
            includeEdges: Optional[bool] = None,
        ) -> SearchQueryResponse:
            """
            Performs a search operation on a specific collection using the provided payload.
            Learn more about usage at: https://gestell.ai/docs/reference#query

            @param collection_id - The ID of the collection to search.
            @param payload - The search parameters, including:
            - `category_id`: An optional category ID to filter results by.
            - `prompt`: The search query or prompt.
            - `method`: An optional search method to use.
            - `type`: An optional search type to specify.
            - `vectorDepth`: An optional depth of vector search.
            - `nodeDepth`: An optional depth of node search.
            - `maxQueries`: An optional maximum number of queries to run.
            - `maxResults`: An optional maximum number of results to return.
            - `includeContent`: A flag to indicate whether to include content in the search results.
            - `includeEdges`: A flag to indicate whether to include edges in the search results.
            @returns A promise that resolves to the search results, including:
            - `status`: The status of the search request.
            - `message`: An optional message providing additional details about the request result.
            - `result`: An array of search results, where each result includes:
            - `content`: The content found in the search.
            - `citation`: The citation or reference for the content.
            - `reason`: The reason or explanation for the result.
            """
            request = SearchQueryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                prompt=prompt,
                method=method,
                type=type,
                vectorDepth=vectorDepth,
                nodeDepth=nodeDepth,
                maxQueries=maxQueries,
                maxResults=maxResults,
                includeContent=includeContent,
                includeEdges=includeEdges,
            )
            response: SearchQueryResponse = await search_query(request)
            return response

        async def prompt(
            self,
            collection_id: str,
            prompt: str,
            category_id: Optional[str] = None,
            method: Optional[SearchMethod] = None,
            type: Optional[SearchType] = None,
            vectorDepth: Optional[int] = None,
            nodeDepth: Optional[int] = None,
            maxQueries: Optional[int] = None,
            maxResults: Optional[int] = None,
            template: Optional[str] = None,
            cot: Optional[bool] = None,
            messages: Optional[list[PromptMessage]] = [],
        ) -> AsyncGenerator[bytes, None]:
            """
            Performs a query operation using a prompt on a specific collection.
            Learn more about usage at: https://gestell.ai/docs/reference#query

            @param collection_id - The ID of the collection to query.
            @param payload - The prompt parameters, including:
            - `category_id`: An optional category ID to filter results by.
            - `prompt`: The prompt or query to execute.
            - `method`: An optional search method to use.
            - `type`: An optional search type to specify.
            - `vectorDepth`: An optional depth of vector search.
            - `nodeDepth`: An optional depth of node search.
            - `maxQueries`: An optional maximum number of queries to run.
            - `maxResults`: An optional maximum number of results to return.
            - `template`: An optional template to use for the prompt.
            - `cot`: A flag indicating whether to use chain-of-thought reasoning (optional).
            - `messages`: The message history for the chat

            @returns A promise that resolves to a readable stream of the prompt query response.
            """
            request = PromptQueryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                prompt=prompt,
                method=method,
                type=type,
                vectorDepth=vectorDepth,
                nodeDepth=nodeDepth,
                maxQueries=maxQueries,
                maxResults=maxResults,
                template=template,
                cot=cot,
                messages=messages,
            )
            async for chunk in prompt_query(request):
                yield chunk

        async def features(
            self,
            collection_id: str,
            category_id: str,
            skip: Optional[int] = 0,
            take: Optional[int] = 10,
        ) -> FeaturesQueryResponse:
            """
            Retrieves feature-related information from a specific collection.
            Learn more about usage at: https://gestell.ai/docs/reference#query

            @param collection_id - The ID of the collection to query.
            @param payload - The features query parameters, including:
            - `category_id`: The ID of the category to retrieve features for.
            - `skip`: An optional parameter to skip a specified number of results (for pagination).
            - `take`: An optional parameter to limit the number of results returned (for pagination).
            @returns A promise that resolves to the features query response, including:
            - `status`: The status of the query request.
            - `message`: An optional message providing additional details about the request result.
            - `result`: An array of `FeatureLayout` objects, where each feature includes:
                - `position`: An array representing the position of the feature.
                - `label`: The label for the feature.
                - `description`: A description of the feature.
            """
            request = FeaturesQueryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                skip=skip,
                take=take,
            )
            response: FeaturesQueryResponse = await featuresQuery(request)
            return response

        async def features_export(
            self, collection_id: str, category_id: str, type: Literal['json', 'csv']
        ) -> any:
            """
            Retrieves features  from a specific collection.
            Learn more about usage at: https://gestell.ai/docs/reference#query

            @param payload - The features query parameters, including:
            - `collection_id`: - The ID of the collection to query
            - `category_id`: The ID of the category to retrieve features for.
            - `type`: Either "json" or "csv" format
            @returns A promise that resolves to a dynamic features array that depends on your category instructions.
            """
            request = ExportFeaturesRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                type=type,
            )
            response: any = await export_features(request)
            return response

        async def table(
            self,
            collection_id: str,
            category_id: str,
            skip: Optional[int] = 0,
            take: Optional[int] = 10,
        ) -> TablesQueryResponse:
            """
            Retrieves table-related information from a specific collection.
            Learn more about usage at: https://gestell.ai/docs/reference#query

            @param payload - The features query parameters, including:
            - `collection_id`: - The ID of the collection to query
            - `category_id`: The ID of the category to retrieve features for.
            - `skip`: An optional parameter to skip a specified number of results (for pagination).
            - `take`: An optional parameter to limit the number of results returned (for pagination).
            @returns A promise that resolves to a dynamic table array that depends on your category instructions.
            """
            request = TablesQueryRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                skip=skip,
                take=take,
            )
            response: TablesQueryResponse = await tables_query(request)
            return response

        async def table_export(
            self, collection_id: str, category_id: str, type: Literal['json', 'csv']
        ) -> any:
            """
            Retrieves table-related information from a specific collection.
            Learn more about usage at: https://gestell.ai/docs/reference#query

            @param payload - The features query parameters, including:
            - `collection_id`: - The ID of the collection to query
            - `category_id`: The ID of the category to retrieve features for.
            - `type`: Either "json" or "csv" format
            @returns A promise that resolves to a dynamic table array that depends on your category instructions.
            """
            request = ExportTableRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                category_id=category_id,
                type=type,
            )
            response: any = await export_table(request)
            return response

    class __Document__:
        """
        Manage documents within a collection. You will need to retrieve the collection id to manage documents.
        Learn more about usage at: https://gestell.ai/docs/reference#document

        @param collection_id - The ID of the collection
        @param document_id - The ID of the document, this is usually required unless creating a document
        """

        def __init__(self, parent: 'Gestell'):
            self.parent = parent

        async def get(
            self, collection_id: str, document_id: str
        ) -> GetDocumentResponse:
            """
            Fetches a specific document from a collection using its unique document ID.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection containing the document.
            @param document_id - The ID of the document to retrieve.
            @returns A promise that resolves to the document details, including:
            - `status`: The status of the request.
            - `message`: An optional message providing additional details about the request result.
            - `result`: An array of `Document` objects, where each document includes:
            - `id`: The unique ID of the document.
            - `collection_id`: The ID of the collection the document belongs to.
            - `path`: The file path of the document.
            - `name`: The name of the document.
            - `type`: The type of the document (e.g., PDF, Word).
            - `layoutType`: The type of layout for the document.
            - `layoutNodes`: The number of layout nodes in the document.
            - `instructions`: Instructions related to the document.
            - `job`: An optional job associated with the document.
            - `layout`: An optional array containing layout details (could be `DocumentLayout[]`, `PhotoLayout[]`, `VideoLayout[]`, or `AudioLayout[]`).
            - `dateCreated`: The creation date of the document.
            - `dateUpdated`: The date the document was last updated.
            """
            request = GetDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                document_id=document_id,
            )
            response: GetDocumentResponse = await get_document(request)
            return response

        async def export(
            self, collection_id: str, document_id: str, type: Literal['json', 'text']
        ) -> any:
            """
            Fetches a specific document from a collection using its unique document ID.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection containing the document.
            @param document_id - The ID of the document to retrieve.
            @param type - JSON or Text
            @returns A promise that resolves to the document in JSON or Text format
            """
            request = ExportDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                document_id=document_id,
                type=type,
            )
            response: any = await export_document(request)
            return response

        async def list(
            self,
            collection_id: str,
            search: Optional[str] = None,
            take: Optional[int] = 10,
            skip: Optional[int] = 0,
            extended: Optional[bool] = None,
            status: Optional[JobStatusType] = None,
            nodes: Optional[JobStatusType] = None,
            edges: Optional[JobStatusType] = None,
            vectors: Optional[JobStatusType] = None,
            category: Optional[JobStatusType] = None,
        ) -> GetDocumentsResponse:
            """
            Fetches a list of documents from a collection, with optional filtering and pagination.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection containing the documents.
            @param payload - Optional parameters for filtering or pagination, including:
            - `search`: A search query string to filter documents.
            - `take`: The number of documents to retrieve.
            - `skip`: The number of documents to skip for pagination.
            - `extended`: Whether to retrieve extended information for the documents.
            - `status`: Filter by the job status type.
            - `nodes`: Filter by the job status for nodes.
            - `edges`: Filter by the job status for edges.
            - `vectors`: Filter by the job status for vectors.
            - `category`: Filter by the job status for category.
            @returns A promise that resolves to the list of documents, including:
            - `status`: The status of the request.
            - `message`: An optional message providing additional details about the request result.
            - `result`: An array of `Document` objects, where each document includes:
            - `id`: The unique ID of the document.
            - `collection_id`: The ID of the collection the document belongs to.
            - `path`: The file path of the document.
            - `name`: The name of the document.
            - `type`: The type of the document (e.g., PDF, Word).
            - `layoutType`: The type of layout for the document.
            - `layoutNodes`: The number of layout nodes in the document.
            - `instructions`: Instructions related to the document.
            - `job`: An optional job associated with the document.
            - `layout`: An optional array containing layout details (could be `DocumentLayout[]`, `PhotoLayout[]`, `VideoLayout[]`, or `AudioLayout[]`).
            - `dateCreated`: The creation date of the document.
            - `dateUpdated`: The date the document was last updated.
            """
            request = GetDocumentsRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=collection_id,
                search=search,
                take=take,
                skip=skip,
                extended=extended,
                status=status,
                nodes=nodes,
                edges=edges,
                vectors=vectors,
                category=category,
            )
            response: GetDocumentsResponse = await list_documents(request)
            return response

        async def upload(
            self,
            collection_id: str,
            name: str,
            file: Union[str, bytes],
            type: Optional[str] = None,
            instructions: Optional[str] = None,
            job: Optional[bool] = None,
            tables: Optional[bool] = None,
        ) -> UploadDocumentResponse:
            """
            Uploads a document to a collection.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param payload - The details of the document to upload, including:
            - `collection_id`: The ID of the collection to upload the document to.
            - `name`: The name of the document.
            - `file`: The file to upload, can be a path string or bytes.
            - `type`: The type of the file (e.g., "text/plain").
            - `instructions`: Optional instructions for the document.
            - `job`: A boolean to indicate if the document should start processing immediately.
            - `tables`: A boolean that flags for additional table processing and analysis is performed on the document, use this for pdfs with complex tables

            @returns A promise that resolves to the response of the document upload, including:
            - `status`: The status of the request (`OK` or `ERROR`).
            - `message`: An optional message providing additional details about the request result.
            - `id`: The ID of the created document.
            """
            request = UploadDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                name=name,
                file=file,
                type=type,
                instructions=instructions,
                job=job,
                tables=tables,
            )
            response: UploadDocumentResponse = await upload_document(request)
            return response

        async def presign(
            self,
            collection_id: str,
            filename: str,
            type: str,
        ) -> PresignDocumentResponse:
            """
            Fetches a pre-signed URL for uploading a document to a collection.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection for the document upload.
            @param payload - The document upload request details, including:
            - `filename`: The name of the document file to upload.
            - `type`: The MIME type of the document (e.g., 'application/pdf').
            @returns A promise that resolves to the pre-signed URL response, including:
            - `status`: The status of the request.
            - `message`: An optional message providing additional details about the request result.
            - `path`: The path where the document will be uploaded.
            - `url`: The pre-signed URL for uploading the document.
            """
            request = PresignDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=collection_id,
                filename=filename,
                type=type,
            )
            response: PresignDocumentResponse = await presign_document(request)
            return response

        async def create(
            self,
            collection_id: str,
            name: str,
            path: str,
            type: str,
            instructions: Optional[str] = None,
            job: Optional[bool] = None,
            tables: Optional[bool] = None,
        ) -> CreateDocumentResponse:
            """
            Allows the creation of a new document in a collection by providing the document details in the payload.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection where the document will be created.
            @param payload - The details of the document to create, including:
            - `name`: The name of the document.
            - `path`: The file path of the document.
            - `type`: The MIME type of the document (e.g., 'application/pdf').
            - `instructions` (optional): Additional instructions related to the document.
            - `job` (optional): Set to false to not dispatch a job
             - `tables`: A boolean that flags for additional table processing and analysis is performed on the document, use this for pdfs with complex tables

            @returns A promise that resolves to the response of the document creation request, including:
            - `status`: The status of the document creation request.
            - `message`: An optional message providing additional details about the request result.
            - `id`: The unique identifier of the created document.
            """
            request = CreateDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                name=name,
                path=path,
                type=type,
                instructions=instructions,
                job=job,
                tables=tables,
            )
            response: CreateDocumentResponse = await create_document(request)
            return response

        async def update(
            self,
            collection_id: str,
            document_id: str,
            name: Optional[str] = None,
            instructions: Optional[str] = None,
            job: Optional[bool] = None,
            tables: Optional[bool] = None,
        ) -> BaseResponse:
            """
            Allows the updating of a document’s details in a collection. Requires the document ID and updated information.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection containing the document.
            @param document_id - The ID of the document to update.
            @param payload - The updated document details, including:
            - `name` (optional): The updated name of the document.
            - `instructions` (optional): Updated instructions related to the document.
            - `job` (optional): Set to true to dispatch a reprocessing job
            - `tables`: A boolean that flags for additional table processing and analysis is performed on the document, use this for pdfs with complex tables

            @returns A promise that resolves to the response of the update request, including:
            - `status`: The status of the update request.
            - `message`: An optional message providing additional details about the update result.
            """
            request = UpdateDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                id=collection_id,
                document_id=document_id,
                name=name,
                instructions=instructions,
                job=job,
                tables=tables,
            )
            response: BaseResponse = await update_document(request)
            return response

        async def delete(self, collection_id: str, document_id: str) -> BaseResponse:
            """
            Deletes an existing document from a collection based on its unique document ID.
            Learn more about usage at: https://gestell.ai/docs/reference#document

            @param collection_id - The ID of the collection containing the document.
            @param document_id - The ID of the document to delete.
            @returns A promise that resolves to the response of the delete request, including:
            - `status`: The status of the delete request.
            - `message`: An optional message providing additional details about the delete result.
            """
            request = DeleteDocumentRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                document_id=document_id,
            )
            response: BaseResponse = await delete_document(request)
            return response

    class __Job__:
        """
        Manage jobs within a collection. You will need to retrieve the collection id to manage jobs.
        Learn more about usage at: https://gestell.ai/docs/reference#job

        @param collection_id - The ID of the collection
        """

        def __init__(self, parent: 'Gestell'):
            self.parent = parent

        async def get(self, collection_id: str, document_id: str) -> GetJobResponse:
            """
            Fetches the details of a job using its unique job ID.
            Learn more about usage at: https://gestell.ai/docs/reference#job

            @param collection_id - The ID of the collection where the job exists.
            @param document_id - The document id for the job to retrieve.
            @returns A promise that resolves to the job details, including:
            - `status`: The status of the job.
            - `message`: An optional message providing additional details about the job.
            - `result`: The detailed job information, including:
                - `id`: The job's unique ID.
                - `collection_id`: The collection to which the job belongs.
                - `document_id`: The associated document ID.
                - `status`: The current status of the job.
                - `nodes`, `edges`, `vectors`, `category`: The job status for each of these components.
                - `message`: A message providing job status details.
                - `dateCreated`: The date the job was created.
                - `dateUpdated`: The date the job was last updated.
            """
            request = GetJobRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                document_id=document_id,
            )
            response: GetJobResponse = await get_job(request)
            return response

        async def list(
            self,
            collection_id: str,
            take: Optional[int] = 10,
            skip: Optional[int] = 0,
            status: Optional[JobStatusType] = 'all',
            nodes: Optional[JobStatusType] = 'all',
            edges: Optional[JobStatusType] = 'all',
            vectors: Optional[JobStatusType] = 'all',
            category: Optional[JobStatusType] = 'all',
        ) -> GetJobsResponse:
            """
            Fetches a list of jobs associated with a collection, with optional filtering or pagination.
            Learn more about usage at: https://gestell.ai/docs/reference#job

            @param collection_id - The ID of the collection for which to fetch jobs.
            @param payload - Optional parameters for filtering or pagination.
            @returns A promise that resolves to a list of jobs.
            """
            request = GetJobsRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                take=take,
                skip=skip,
                status=status,
                nodes=nodes,
                edges=edges,
                vectors=vectors,
                category=category,
            )
            response: GetJobsResponse = await list_jobs(request)
            return response

        async def reprocess(
            self, collection_id: str, ids: List[str], type: JobType
        ) -> ReprocessDocumentsResponse:
            """
            Initiates a new job in the collection based on the provided parameters.
            Learn more about usage at: https://gestell.ai/docs/reference#job

            @param collection_id - The ID of the collection where the job will be created.
            @param payload - The job creation parameters, including:
            - `ids`: An array of document ids to dispatch a reprocess job for
            - `type`: The type of job to reprocess for ('status', 'nodes', 'vectors', 'edges', 'category').
            @returns A promise that resolves to the response of the job creation request, including:
            - `status`: The result status of the job creation request.
            - `message`: An optional message providing additional details about the job creation.
            """
            request = ReprocessDocumentsRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                ids=ids,
                type=type,
            )
            response: ReprocessDocumentsResponse = await reprocess_document(request)
            return response

        async def cancel(self, collection_id: str, ids: List[str]) -> BaseResponse:
            """
            Deletes an existing job from a collection based on the unique job IDs.
            Learn more about usage at: https://gestell.ai/docs/reference#job

            @param collection_id - The ID of the collection where the job exists.
            @param job_ids[] - The IDs of the jobs to delete.
            @returns A promise that resolves to the response of the job deletion request, including:
            - `status`: The result status of the job deletion request.
            - `message`: An optional message providing additional details about the job deletion.
            """
            request = CancelJobsRequest(
                api_key=self.parent.api_key,
                api_url=self.parent.api_url,
                debug=self.parent.debug,
                collection_id=collection_id,
                ids=ids,
            )
            response: CancelJobsResponse = await cancel_jobs(request)
            return response
