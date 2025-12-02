from http import HTTPStatus
from flask import jsonify, Flask

app = Flask(__name__)
app.app_context().push()

with app.app_context():
    
    OK_MSG = jsonify({"msg": "Request successfully made"}), HTTPStatus.OK
    BAD_REQUEST_MSG = jsonify({"msg": "Incorrect or missing parameters"}), HTTPStatus.BAD_REQUEST
    UNAUTHORIZED_MSG = jsonify({"msg": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED
    INTERNAL_SERVER_ERROR_MSG = jsonify({"msg": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    BAD_REQUEST_EMPTY_LOGIN_MSG = jsonify({"msg": "Bad request. Username and password are mandatory fields", "code": "1001"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_USERNAME_LOGIN_MSG = jsonify({"msg": "Bad request. Username is a mandatory field", "code": "1002"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_PASSWORD_LOGIN_MSG = jsonify({"msg": "Bad request. Password is a mandatory field", "code": "1003"}), HTTPStatus.BAD_REQUEST
    USER_NOT_FOUND_MSG = jsonify({"msg": "The user is not found", "code":"1004"}), HTTPStatus.NOT_FOUND
    UNAUTHORIZED_LOGIN_MSG = jsonify({"msg": "Unauthorized. The credentials are wrong", "code":"1005"}), HTTPStatus.UNAUTHORIZED
    UNAUTHORIZED_NOT_ADMIN_MSG = jsonify({"msg": "Unauthorized. JWT missing or invalid", "code":"1006"}), HTTPStatus.UNAUTHORIZED
    FORBIDDEN_ACTION_NOT_ADMIN_MSG = jsonify({"msg": "Forbidden. You do not have admin permissions", "code":"1007"}), HTTPStatus.FORBIDDEN
    SUCCESS_UNBLOCK_USER_MSG = jsonify({"msg":"User has been unblocked", "code":"1009"}), HTTPStatus.OK
    SUCCESS_RECTIFY_DELETE_USER_MSG = jsonify({"msg":"User delete has been rectified", "code":"1010"}), HTTPStatus.OK
    CAN_NOT_BLOCK_AN_ADMIN = jsonify({"msg":"Admin can not be blocked", "code":"1011"}), HTTPStatus.FORBIDDEN
    CAN_NOT_DELETE_AN_ADMIN = jsonify({"msg":"Admin can not be deletd", "code":"1012"}), HTTPStatus.FORBIDDEN
    BLOCKED_USER_CAN_NOT_LOGIN_MSG = jsonify({"msg":"Forbidden. User blocked can not login", "code":"1013"}), HTTPStatus.FORBIDDEN
    DELETED_USER_CAN_NOT_LOGIN_MSG = jsonify({"msg":"Forbidden. User deleted can not login","code":"1014"}), HTTPStatus.FORBIDDEN
    
    BAD_REQUEST_EMPTY_REGISTER_MSG = jsonify({"msg": "Bad request. All the fields are mandatory","code":"2001"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_PASSWORD_MISMATCH_REGISTER_MSG = jsonify({"msg": "Bad request. Passwords do not match", "code":"2002"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_INVALID_PASSWORD_REGISTER_MSG = jsonify({"msg": "Bad request. The password is invalid", "code":"2003"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_INVALID_DATE_REGISTER_MSG = jsonify({"msg":"Bad request. Invalid date format", "code":"2004"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_UNDERAGE_REGISTER_MSG = jsonify({"msg": "Bad request. The user must be over 14", "code":"2005"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_USERNAME_ALREADY_EXISTS_REGISTER_MSG = jsonify({"msg": "Bad request. The username already exists", "code":"2006"}), HTTPStatus.BAD_REQUEST
    USER_CORRECT_REGISTER_MSG = ({"msg": "Created. The user was registered correctly", "code":"2007"}), HTTPStatus.CREATED

    BAD_REQUEST_EMPTY_RECOVER_PASSWORD_MSG = jsonify({"msg": "Bad request. All the fields are mandatory","code":"3001"}), HTTPStatus.BAD_REQUEST
    USER_FOUND_RECOVER_PASSWORD_MSG = jsonify({"msg":"User was found", "code":"3002"}), HTTPStatus.OK
    BAD_REQUEST_ANSWER_MISMATCH_RECOVER_PASSWORD_MSG = jsonify({"msg":"Bad request. The answer does not match","code":"3003"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_PASSWORD_MISMATCH_RECOVER_PASSWORD_MSG = jsonify({"msg": "Bad request. Passwords do not match", "code":"3004"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_INVALID_PASSWORD_RECOVER_PASSWORD_MSG = jsonify({"msg": "Bad request. The password is invalid", "code":"3005"}), HTTPStatus.BAD_REQUEST
    USER_PASSWORD_UPDATED_MSG = jsonify({"msg": "The password was updated correctly", "code":"3006"}), HTTPStatus.OK
    BAD_REQUEST_USERNAME_NOT_FOUND_MSG = jsonify({"msg": "Bad request. The username was not found", "code":"3007"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_SAME_PASSWORD_RECOVER_PASSWORD_MSG= jsonify({"msg": "Bad request. The new password is already in use", "code": "3008"}), HTTPStatus.BAD_REQUEST
    
    BAD_REQUEST_BOOK_NOT_FOUND_UPLOAD_BOOK = jsonify({"msg": "Bad request. File was not found","code":"4001"}), HTTPStatus.NOT_FOUND
    BAD_REQUEST_USER_NOT_FOUND_UPLOAD_BOOK = jsonify({"msg": "Bad request. File was not found","code":"4002"}), HTTPStatus.NOT_FOUND
    BAD_REQUEST_INVALID_FILE_UPLOAD_BOOK = jsonify({"msg": "Bad request. Invalid file","code":"4003"}), HTTPStatus.BAD_REQUEST
    BAD_REQUEST_BOOK_NOT_FOUND_DELETE_MSG = jsonify({"msg": "Bad request. Book has not been found","code":"4004"}), HTTPStatus.NOT_FOUND
    BAD_REQUEST_USER_NOT_FOUND_DELETE_MSG = jsonify({"msg": "Bad request. User has not been found","code":"4005"}), HTTPStatus.NOT_FOUND
    BAD_REQUEST_BOOK_COULD_NOT_BE_DELETED_MSG = jsonify({"msg": "Bad request. Book could not be deleted", "code":"4005"}), HTTPStatus.BAD_REQUEST
    BOOK_CORRECT_DELETE_MSG = jsonify({"msg": "Success. The book has been deleted correctly", "code":"4007"}), HTTPStatus.OK
    ERROR_DELETING_BOOK_MSG = jsonify({"msg": "Error while deleting the book", "code":"4008"}), HTTPStatus.INTERNAL_SERVER_ERROR
    BOOK_NOT_FOUND_DOWNLOAD_MSG = jsonify({"msg": "Book has not been found","code":"4009"}), HTTPStatus.NOT_FOUND
    BAD_REQUEST_BOOK_HAS_NOT_FILE_MSG = jsonify({"msg": "Bad request. Book has not an associated file","code":"4010"}), HTTPStatus.BAD_REQUEST    
    BOOK_FILE_NOT_FOUND_MSG = jsonify({"msg": "Book file has not been found","code":"4011"}), HTTPStatus.NOT_FOUND
    DOWNLOAD_BOOK_ERROR_MSG = jsonify({"msg": "Error while downloading the book", "code":"4012"}), HTTPStatus.INTERNAL_SERVER_ERROR
    BAD_REQUEST_USER_ID_NOT_FOUND_MSG = jsonify({"msg": "Bad request. There is not id_user","code":"4013"}), HTTPStatus.BAD_REQUEST
    SEARCH_USER_ERROR_MSG = jsonify({"msg": "Error in the search", "code":"4014"}), HTTPStatus.INTERNAL_SERVER_ERROR
    COVER_NOT_FOUND_MSG = jsonify({"msg": "Book cover was not found", "code":"4015"}), HTTPStatus.NOT_FOUND
    BOOK_NOT_FOUND_MSG = jsonify({"msg": "Book not found ", "code":"4016"}), HTTPStatus.NOT_FOUND
    GET_DETAIL_BOOK_ERROR_MSG = jsonify({"msg": "Error getting the book detail", "code":"4017"}), HTTPStatus.INTERNAL_SERVER_ERROR
    NOT_FULL_DATA_CREATE_REVIEW_MSG = jsonify({"msg": "Bad request. Some data is missing", "code":"4018"}), HTTPStatus.BAD_REQUEST
    NO_BOOK_REVIEWS_MSG = jsonify({"msg": "There are not reviews for this book", "code":"4019"}), HTTPStatus.OK
    REVIEW_NOT_FOUND_MSG = jsonify({"msg": "Review not found", "code":"4020"}), HTTPStatus.NOT_FOUND
    REVIEW_DELETED_MSG = jsonify({"msg": "Review deleted correctly", "code":"4021"}), HTTPStatus.OK
    REVIEW_DELETED_ERROR_MSG = jsonify({"msg": "Error deleting the review", "code":"4022"}), HTTPStatus.INTERNAL_SERVER_ERROR
    BAD_REQUEST_INVALID_RATING_MSG = jsonify({"msg": "Bad request. The rating is invalid (it must be 5 in the body as maximum)", "code":"4023"}), HTTPStatus.BAD_REQUEST