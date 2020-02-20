#include <mysql.h>
#include <iostream>

using namespace std;

MYSQL *conn;
MYSQL_RES *res;
MYSQL_ROW row;


// argv = [program, host, user, password, db, port, coupon_code]
int main(int argc, char **argv)	{
	if (argc != 7){
		cerr << "Call Error: wrong number of parameters [program, host, user, password, db, port, coupon_code]" << endl;
		return 1;
	}
	//printf("Working!\n");

	string coupon_code = argv[6];
	// string coupon_code = "coupon1";

	conn = mysql_init(0);
	char *_end;
	conn = mysql_real_connect(conn, argv[1], argv[2], argv[3], argv[4], strtoul(argv[5], &_end, 10), NULL, 0);
	//conn = mysql_real_connect(conn, "localhost", "root", "root", "db_ecommerce", 3306, NULL, 0);
	if (!conn){
		cerr << "Connection Error: " << mysql_error(conn) << endl;
		//getchar();
		mysql_close(conn);
		return 1;
	}

	string query_str = "SELECT `idCoupon`, `value` FROM `Coupon` WHERE `idCoupon`='" + coupon_code + "';";
	if (mysql_query(conn, query_str.c_str())){
		cerr << "Query Error: " << mysql_error(conn) << endl;
		//getchar();
		mysql_close(conn);
		return 1;
	}

	res = mysql_use_result(conn);
	if ((row = mysql_fetch_row(res)) != NULL){
		cout << row[0] << " " << row[1] << endl;
	} else {
		cout << "None" << endl;
	}
	mysql_free_result(res);
	mysql_close(conn);

	//getchar();
	return 0;
}