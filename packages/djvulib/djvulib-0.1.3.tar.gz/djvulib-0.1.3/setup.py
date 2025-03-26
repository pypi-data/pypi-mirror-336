from distutils.core import setup, Extension

setup(name="djvulib",
      version="0.1.3",
      ext_modules = [
        Extension('djvulib', ["djvulib.cpp", "djvu.cpp","Arrays.cpp", "DjVmNav.cpp", "DjVuGlobal.cpp", "DjVuPort.cpp", "GOS.cpp", "GUnicode.cpp", "MMX.cpp", "miniexp.cpp", "BSByteStream.cpp", "DjVuAnno.cpp", "DjVuGlobalMemory.cpp", "DjVuText.cpp", "GPixmap.cpp", "IFFByteStream.cpp", "UnicodeByteStream.cpp", "BSEncodeByteStream.cpp", "DjVuDocEditor.cpp", "DjVuImage.cpp", "DjVuToPS.cpp", "GRect.cpp", "IW44EncodeCodec.cpp", "XMLParser.cpp", "ByteStream.cpp", "DjVuDocument.cpp", "DjVuInfo.cpp", "GBitmap.cpp", "GScaler.cpp", "IW44Image.cpp", "XMLTags.cpp", "DataPool.cpp", "DjVuDumpHelper.cpp", "DjVuMessage.cpp", "GContainer.cpp", "GSmartPointer.cpp", "JB2EncodeCodec.cpp", "ZPCodec.cpp", "DjVmDir.cpp", "DjVuErrorList.cpp", "DjVuMessageLite.cpp", "GException.cpp", "GString.cpp", "JB2Image.cpp", "atomic.cpp", "DjVmDir0.cpp", "DjVuFile.cpp", "DjVuNavDir.cpp", "GIFFManager.cpp", "GThreads.cpp", "JPEGDecoder.cpp", "ddjvuapi.cpp", "DjVmDoc.cpp", "DjVuFileCache.cpp", "DjVuPalette.cpp", "GMapAreas.cpp", "GURL.cpp", "MMRDecoder.cpp", "debug.cpp"], define_macros=[("HAVE_CONFIG_H", "1")], libraries=[], extra_compile_args=["-std=c++14"], include_dirs=[])
    ]
)
