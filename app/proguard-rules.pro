# 출시 빌드(난독화·축소) 규칙
# kotlinx.serialization: 라이브러리 기본 규칙 + 우리 데이터 클래스의 직렬화 정보 보존
-keepattributes *Annotation*, InnerClasses, Signature
-dontnote kotlinx.serialization.**
-keepclassmembers @kotlinx.serialization.Serializable class com.aijoso.app.** {
    *** Companion;
    *** serializer(...);
    <fields>;
}
-keep,includedescriptorclasses class com.aijoso.app.**$$serializer { *; }
