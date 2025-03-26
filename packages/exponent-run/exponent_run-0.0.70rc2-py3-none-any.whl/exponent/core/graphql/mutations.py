HALT_CHAT_STREAM_MUTATION: str = """
  mutation HaltChatStream($chatUuid: UUID!) {
    haltChatStream(chatUuid: $chatUuid) {
      __typename
    }
  }
"""


SET_LOGIN_COMPLETE_MUTATION: str = """
  mutation SetLoginComplete {
    setLoginComplete {
      __typename
      ... on User {
        userApiKey
      }
      ... on UnauthenticatedError {
        message
      }
    }
  }
"""


REFRESH_API_KEY_MUTATION = """
mutation RefreshApiKey {
    refreshApiKey {
        ... on User {
            userApiKey
        }
        ... on UnauthenticatedError {
            message
        }
    }
}
"""
