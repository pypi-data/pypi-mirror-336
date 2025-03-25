#include <Python.h>

/* 定义模块信息 */
static struct PyModuleDef dummy_module = {
    PyModuleDef_HEAD_INIT,
    "_dummy",   /* 模块名称，必须与扩展模块名称中后半部分一致 */
    "Dummy module for platform tagging",  /* 模块文档 */
    -1,         /* 模块状态大小 */
    NULL        /* 模块方法表，此处为空 */
};

/* 初始化函数，名称必须为 PyInit__dummy */
PyMODINIT_FUNC PyInit__dummy(void) {
    return PyModule_Create(&dummy_module);
}
