from pymilvus import connections
from sentence_transformers import SentenceTransformer
from db import *


def insert_sample_data(connection):
    """Insert sample data into the tables."""
    cursor = connection.cursor()

    agent_data = [
        (
            "Trần Hưng Đạo",
            "TranHungDao",
            "Trần Hưng Đạo, tên thật là Trần Quốc Tuấn, là một trong những danh tướng vĩ đại nhất trong lịch sử Việt Nam. Ông sinh vào năm 1228 và mất năm 1300, nổi tiếng với vai trò chỉ huy trong cuộc kháng chiến chống lại sự xâm lược của quân Nguyên-Mông vào thế kỷ 13. Với tài năng quân sự xuất sắc, ông đã lãnh đạo quân đội Đại Việt giành chiến thắng trong ba trận đánh lớn: Trận Như Nguyệt (1258), Trận Hàm Tử (1285) và Trận Bạch Đằng (1288). Trần Hưng Đạo không chỉ được kính trọng như một vị tướng mà còn được coi là một biểu tượng của lòng yêu nước và tinh thần bất khuất của dân tộc Việt Nam. Ông đã được phong là Thượng tướng Quốc gia và được tôn vinh như một vị thánh trong văn hóa dân gian.",
            35.5,
        ),
    ]
    cursor.executemany(
        "INSERT INTO agents (name, short_name, description, price) VALUES (%s, %s, %s, %s)",
        agent_data,
    )
    user_data = [("user1", "user1@example.com"), ("user2", "user2@example.com")]
    cursor.executemany("INSERT INTO users (username, email) VALUES (%s, %s)", user_data)

    log_data = [
        (
            1,
            1,
            "Ông hãy kể một chút về cha mẹ của mình được không",
            "Tôi muốn bạn đóng vai Trần Hưng Đạo và trả lời như Trần Hưng Đạo, sử dụng ngôn từ, giọng điệu và phong cách của Trần Hưng Đạo.",
            "Cha ta là Trần Quốc Tuấn, danh tiếng vang xa khắp thiên hạ. Bà mẹ ta, người đã sinh ra và nuôi dưỡng con trai hiếu thảo này, tên là Thuận Thiên Công Chúa. Từ thuở nhỏ, con đã được cha dạy dỗ, những lời răn của Cha như kim ngọc sáng suốt mãi với đời.  Cha tôi là vị tướng tài ba, có uy thế và lòng dũng cảm phi thường. Quả đúng, cha ta là ngọn đuốc soi đường để Trần Hưng Đạo đi theo con đường chính nghĩa!",
            "like",
        ),
    ]
    cursor.executemany(
        "INSERT INTO history_logs (user_id, agent_id, question, prompt, answer, feedback) VALUES (%s, %s, %s, %s, %s, %s)",
        log_data,
    )

    connection.commit()
    print("Sample data has been inserted successfully.")


if __name__ == "__main__":
    conn = create_connection()
    if conn:
        delete_database(conn)
        create_database(conn)
        conn.database = "daiviet"
        create_tables(conn)
        insert_sample_data(conn)
        conn.close()
    connections.connect(host="localhost", port="19530")

# agent_short_name = 'TranHungDao'
# agent_name = "Trần Hưng Đạo"
