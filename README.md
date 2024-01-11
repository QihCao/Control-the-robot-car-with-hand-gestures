Điều khiển robot bằng cử chỉ tay (số đếm ngón tay) bằng giao thức MQTT với các chức năng:
 + 0 - stop
 + 1 - left
 + 2 - right
 + 4 - backward
 + 5 - forward

Phần cứng:
  + Raspberry Pi (Có thể thay thế bằng ESP32)
  + L298N
  + Động cơ DC

IDE để lập trình:
  + Pycharm / VScode
  + Thonny (tích hợp sẵn trên Rasp)

Cách chạy chương trình:
  + Khởi tạo kết nối MQTT (chạy file mqtts.py trên Pycharm và mqtt.c trên Rasp)
  + Lần lượt chạy 2 file main.py trên Pycharm và Ras
