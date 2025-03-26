#include "guarded_pool_allocator_tls.h"
#include "wrapper.h"
#include "ddjvuapi.h"

namespace gwp_asan {
ThreadLocalPackedVariables *getThreadLocals() {
  alignas(8) static GWP_ASAN_TLS_INITIAL_EXEC ThreadLocalPackedVariables Locals;
  return &Locals;
}
}

void handleMessages(ddjvu_context_t *ctx) {
    const ddjvu_message_t *msg;
    while ((msg = ddjvu_message_peek(ctx))) {
        switch (msg->m_any.tag) {
            case DDJVU_ERROR:
                // ThrowDjvuError(env, msg);
                break;
            case DDJVU_INFO:
                break;
            case DDJVU_DOCINFO:
                break;
            default:
                break;
        }
        ddjvu_message_pop(ctx);
    }
}

void waitAndHandleMessages(ddjvu_context_t *contextHandle) {
    ddjvu_context_t *ctx = contextHandle;
    // Wait for first message
    ddjvu_message_wait(ctx);
    // Process available messages
    handleMessages(ctx);
}

int get_djvu_number_of_pages(char* nativePath) {
    ddjvu_context_t *ctx = ddjvu_context_create("djvu");
    ddjvu_document_t *doc = ddjvu_document_create_by_filename(ctx, nativePath, TRUE);
    ddjvu_message_wait(ctx);
    while (ddjvu_message_peek(ctx)) {
        if (ddjvu_document_decoding_done(doc)) {
            break;
        }
        ddjvu_message_pop(ctx);
    }
    int n = ddjvu_document_get_pagenum(doc);
    ddjvu_document_release(doc);
    ddjvu_context_release(ctx);
    return n;
}

djvu_document get_djvu_page(int pageno, char* nativePath) {
    ddjvu_context_t *ctx = ddjvu_context_create("djvu");
    ddjvu_document_t *doc = ddjvu_document_create_by_filename(ctx, nativePath, TRUE);
    ddjvu_message_wait(ctx);
    while (ddjvu_message_peek(ctx)) {
        if (ddjvu_document_decoding_done(doc)) {
            break;
        }
        ddjvu_message_pop(ctx);
    }
   ddjvu_page_t *page = ddjvu_page_create_by_pageno(doc, pageno);

    ddjvu_status_t r;
    ddjvu_pageinfo_t info;
    while ((r = ddjvu_document_get_pageinfo(doc, pageno, &info)) < DDJVU_JOB_OK) {
    }

    int w = info.width;
    int h = info.height;

    ddjvu_rect_t rrect;
    ddjvu_rect_t prect;

    prect.x = 0;
    prect.y = 0;
    prect.w = w;

    prect.h = h;
    rrect = prect;

    unsigned int masks[] = {0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000};
    ddjvu_format_t *pixelFormat = ddjvu_format_create(DDJVU_FORMAT_GREY8, 0, NULL);

    ddjvu_format_set_row_order(pixelFormat, 1);
    ddjvu_format_set_y_direction(pixelFormat, 1);

    int size = w * h;
    char* pixels = (char *) malloc(size);

    while (!ddjvu_page_decoding_done(page)) {
        waitAndHandleMessages(ctx);
    }

    int strade = w;
    ddjvu_page_render(page, DDJVU_RENDER_COLOR,
                                     &prect,
                                     &rrect,
                                     pixelFormat,
                                     strade,
                                      pixels);

    ddjvu_format_release(pixelFormat);
    ddjvu_document_release(doc);
    ddjvu_context_release(ctx);
    djvu_document ddoc;
    ddoc.width = w;
    ddoc.height = h;
    ddoc.pixels = pixels;
    return ddoc;
  
}
