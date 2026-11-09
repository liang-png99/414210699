program sum_n                                   ! 主程式開始，名稱為 sum_n
  implicit none                                 ! 關閉隱含型別，所有變數都必須明確宣告
  integer(8) :: n, i, total                     ! 8 位元組整數：n 為上限，i 為迴圈計數，total 為累加總和
  character(len=32) :: arg                      ! 用來接收命令列參數的字串（最長 32 字元）
  integer :: ios                                ! 讀取狀態碼：0 代表成功，非 0 代表失敗

  if (command_argument_count() >= 1) then       ! 若使用者在命令列有給參數
    call get_command_argument(1, arg)           ! 取出第 1 個參數，存入 arg
    read(arg, *, iostat=ios) n                  ! 把字串轉成整數存入 n，結果狀態存入 ios
  else                                          ! 否則（沒有給參數）
    write(*, '(A)', advance='no') 'Enter N: '   ! 印出提示文字，且不換行
    read(*, *, iostat=ios) n                    ! 從鍵盤讀入 n，結果狀態存入 ios
  end if                                        ! 結束輸入方式的判斷

  if (ios /= 0 .or. n < 1) then                 ! 若讀取失敗，或 n 小於 1（不合法）
    write(*, '(A)') 'Error: N must be a positive integer.'  ! 印出錯誤訊息
    stop 1                                      ! 以結束碼 1 終止程式，表示異常結束
  end if                                        ! 結束輸入檢查

  total = 0                                     ! 累加器歸零
  do i = 1, n                                   ! 迴圈：i 從 1 跑到 n
    total = total + i                           ! 把目前的 i 加進總和
  end do                                        ! 結束迴圈

  write(*, '(A,I0,A,I0)') 'Sum of 1 to ', n, ' = ', total  ! 輸出結果，I0 代表整數用最短寬度顯示
end program sum_n                               ! 主程式結束
